import openai
from datetime import datetime
from dateutil import tz

# pylint: disable=import-error
from src.controller.analysis_server.schema.post_chat_msg import (
    PostChatMsgRequestBody,
    PostChatMsgResponseBody,
)
from src.controller.analysis_server.schema.post_report_msg import (
    PostReportMsgRequestBody,
    PostReportMsgResponseBody,
)
from src.dependencies.settings import get_settings
from src.entity.employee_entity import Employee
from src.entity.enter_record_entity import EnterRecord
from src.entity.machine_record_entity import MachineRecord
from src.infra.repo.analysis_server_repo import AnalysisServerRepo
from src.service.enter_record_service import EnterRecordService


class AnalysisServerService:
    def __init__(self) -> None:
        setting = get_settings()
        openai.api_key = setting.gpt_secret_key

        # 由聊天問句生成資料庫 query
        self.userSchemaMsg = "Employee schema: " + Employee.brief()
        self.enterRecordSchemaMsg = "EnterRecord schema: " + EnterRecord.brief()
        self.machineRecordSchemaMsg = "MachineRecord Schema: " + MachineRecord.brief()
        self.lateDefinitionMsg = "To know an employee is late or not, covert the date into hour and minute and compare it with the shift time, if the enter_time greater than shift_time, he is late."
        self.dataFunctionMsg = "Data function: AnalysisServerRepo().getData(collection, query), the function will find(query) in the db collection"
        self.codeExampleMsg = 'Code example: data = AnalysisServerRepo().getData("Employee", {"department": "HQ"}), X = len(data)'
        self.retQueryMsg = "Use the data function to answer the following question, and store the result in variable 'X'. Return python code only"

        # 由 db 資料跟問句生成回答
        self.dataFoundMsg = "The finding data is: "
        self.codeQueryMsg = "The code to get the data is: "
        self.dateDefinitionMsg = "Don't return the timestamp, instead convert to format MM/DD/YYYY hh:mm. For example: convert 1694994480 to 09/18/2023 07:48"
        self.retUserMsg = (
            "Please use the finding data to answer the following question in "
        )

        # 由遲到分布資料生成觀察跟結論
        self.reportQuestionMsg = "List 2 ~ 3 observation from the following data with explanation briefly (less than 300 words). All in {0}"
        self.reportAttedencePrefixMsg = "The user is a HR in the company, who wants to know about the attendance of the employee."
        self.reportTotalLateDataMsg = "The data shows the distribution of late, on time and early employee from {0} to {1}"
        self.reportDeptLateDataMsg = "The data shows the distribution of late, on time and early employee of each department from {0} to {1}"
        self.reportAttedenceConclusionMsg = (
            "Draw a summary of the informations as the ending of the report. All in {0}"
        )

        # 由掃描資料生成觀察跟結論
        self.reportMachinePrefixMsg = "The data are from a security gate's tool scan machine, it check the employee bring some danger items into the workspace."
        self.reportDangerLevelMsg = "The data shows the distribution of the normal, warning and danger status of employee's belongings from {0} to {1}"
        self.reportDangerCountMsg = "The data shows the distribution of the identified contraband found in employee's belongings from {0} to {1}"
        self.reportMachineConclusionMsg = (
            "Draw a summary of the informations as the ending of the report. All in {0}"
        )
        

    def gpt(self, messages):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
            max_tokens=512,
            temperature=0.5,
            n=1,
        )
        return completion.choices[0].message.content

    # chatting system
    def chat_with_GPT(self, body: PostChatMsgRequestBody):
        question = body.message
        language = body.language

        queryMsg = self.text2mongoQuery(question)
        # queryMsg = 'data = AnalysisServerRepo().getData(\"EnterRecord\", {\"employee_id\": \"EMP001\"})\nX = data[0][\"enter_time\"]\nX'
        # return PostChatMsgResponseBody(**{"message": queryMsg})

        vars = {}
        try:
            exec(queryMsg, globals(), vars)
            # return PostChatMsgResponseBody(**{"message": str(vars)})
        except:
            return PostChatMsgResponseBody(**{"message": queryMsg + " exec() failed!"})

        ret = self.data2retMsg(question, language, vars, queryMsg)
        return PostChatMsgResponseBody(**{"message": ret})

    def text2mongoQuery(self, question):
        messages = []
        messages.append({"role": "system", "content": self.userSchemaMsg})
        messages.append({"role": "system", "content": self.enterRecordSchemaMsg})
        messages.append({"role": "system", "content": self.machineRecordSchemaMsg})
        messages.append({"role": "system", "content": self.lateDefinitionMsg})
        messages.append({"role": "system", "content": self.dataFunctionMsg})
        messages.append({"role": "system", "content": self.codeExampleMsg})
        messages.append({"role": "system", "content": self.retQueryMsg})
        messages.append({"role": "user", "content": question})
        # return str(messages)

        ret = self.gpt(messages)
        return ret

    def data2retMsg(self, question, language, vars, queryMsg):
        messages = []
        messages.append({"role": "system", "content": self.dataFoundMsg + str(vars)})
        messages.append({"role": "system", "content": self.codeQueryMsg + queryMsg})
        messages.append({"role": "system", "content": self.dateDefinitionMsg})
        messages.append({"role": "system", "content": self.retUserMsg + language})
        messages.append({"role": "user", "content": question})
        ret = self.gpt(messages)

        return ret

    def weekly_report_GPT(self, body: PostReportMsgRequestBody):
        reportType = body.type
        startTime = body.start_timestamp
        endTime = body.end_timestamp
        language = body.language

        ret = {}
        title, content = "", []
        if reportType == "attendance":
            title, content = self.attendance_report(startTime, endTime, language)
        elif reportType == "machine":
            title, content = self.machine_report(startTime, endTime, language)
        ret["title"] = title
        ret["content"] = content
        ret["end_timestamp"] = endTime

        return PostReportMsgResponseBody(**ret)

    def timestamp2str(self, timestamp):
        date = datetime.fromtimestamp(timestamp, tz=tz.gettz("Asia/Taipei"))
        return date.strftime("%m/%d/%Y")

    def attendance_report(self, startTime, endTime, language):
        startTimeStr, endTimeStr = self.timestamp2str(startTime), self.timestamp2str(
            endTime
        )
        title = "Attendance Report: " + startTimeStr + " ~ " + endTimeStr
        contents = []

        ers = EnterRecordService()

        totalLateDistribution = []
        deptLateDistribution = []
        day = 86400
        for i in range((endTime - startTime) // day):
            s, e = startTime + day * i, startTime + day * (i + 1)
            totalLateDistribution.append(
                ers.query_total_late_status(start_timestamp=s, end_timestamp=e).model_dump()
            )
            deptLateDistribution.append(
                [
                    x.model_dump()
                    for x in ers.query_department_late_distribution(
                        start_timestamp=s, end_timestamp=e
                    )
                ]
            )

        contents.append(
            self.totalLate2msg(
                totalLateDistribution, startTimeStr, endTimeStr, language
            )
        )
        contents.append(
            self.deptLate2msg(deptLateDistribution, startTimeStr, endTimeStr, language)
        )
        contents.append(self.attendanceConclusionMsg(contents, language))

        return title, contents

    def totalLate2msg(self, totalLateDistribution, startTime, endTime, language):
        messages = []
        messages.append(
            {
                "role": "system",
                "content": self.reportTotalLateDataMsg.format(startTime, endTime),
            }
        )
        messages.append({"role": "system", "content": str(totalLateDistribution)})
        messages.append({"role": "system", "content": self.reportAttedencePrefixMsg})
        messages.append(
            {"role": "user", "content": self.reportQuestionMsg.format(language)}
        )

        ret = self.gpt(messages)
        return ret

    def deptLate2msg(self, deptLateDistribution, startTime, endTime, language):
        messages = []
        messages.append(
            {
                "role": "system",
                "content": self.reportDeptLateDataMsg.format(startTime, endTime),
            }
        )
        messages.append({"role": "system", "content": str(deptLateDistribution)})
        messages.append({"role": "system", "content": self.reportAttedencePrefixMsg})
        messages.append(
            {"role": "user", "content": self.reportQuestionMsg.format(language)}
        )

        ret = self.gpt(messages)
        return ret

    def attendanceConclusionMsg(self, contents, language):
        messages = []
        messages.append({"role": "system", "content": self.reportAttedencePrefixMsg})
        for i in range(len(contents)):
            messages.append(
                {
                    "role": "assistant",
                    "content": "Information from chart {}: ".format(i + 1)
                    + contents[i],
                }
            )
        messages.append(
            {
                "role": "user",
                "content": self.reportAttedenceConclusionMsg.format(language),
            }
        )

        ret = self.gpt(messages)
        return ret

    def machine_report(self, startTime, endTime, language):
        startTimeStr, endTimeStr = self.timestamp2str(startTime), self.timestamp2str(endTime)
        title = "Machine Report: " + self.timestamp2str(startTime) + " ~ " + self.timestamp2str(endTime)
        
        contents = []

        ers = EnterRecordService()

        dangerLevelDistribution = []
        dangerCountDistribution = []
        day = 86400
        for i in range((endTime - startTime) // day):
            s, e = startTime + day * i, startTime + day * (i + 1)
            dangerLevelDistribution.append(
                ers.get_danger_count(start_timestamp=s, end_timestamp=e).model_dump()
            )
            dangerCountDistribution.append(
                ers.get_detailed_danger_count(start_timestamp=s, end_timestamp=e).model_dump()
            )

        contents.append(
            self.dangerLevel2msg(dangerLevelDistribution, startTimeStr, endTimeStr, language)
        )
        contents.append(
            self.dangerCount2msg(dangerCountDistribution, startTimeStr, endTimeStr, language)
        )
        contents.append(self.machineConclusionMsg(contents, language))

        return title, contents

    def dangerLevel2msg(self, dangerLevelDistribution, startTime, endTime, language):
        messages = []
        messages.append(
            {
                "role": "system",
                "content": self.reportDangerLevelMsg.format(startTime, endTime),
            }
        )
        messages.append({"role": "system", "content": str(dangerLevelDistribution)})
        messages.append({"role": "system", "content": self.reportMachinePrefixMsg}) 
        messages.append(
            {"role": "user", "content": self.reportQuestionMsg.format(language)}
        )

        ret = self.gpt(messages)
        return ret
    
    def dangerCount2msg(self, dangerCountDistribution, startTime, endTime, language):
        messages = []
        messages.append(
            {
                "role": "system",
                "content": self.reportDangerCountMsg.format(startTime, endTime),
            }
        )
        messages.append({"role": "system", "content": str(dangerCountDistribution)})
        messages.append({"role": "system", "content": self.reportMachinePrefixMsg}) 
        messages.append(
            {"role": "user", "content": self.reportQuestionMsg.format(language)}
        )

        ret = self.gpt(messages)
        return ret
    
    def machineConclusionMsg(self, contents, language):
        messages = []
        messages.append({"role": "system", "content": self.reportMachinePrefixMsg}) 
        for i in range(len(contents)):
            messages.append(
                {
                    "role": "assistant",
                    "content": "Information from chart {}: ".format(i + 1)
                    + contents[i],
                }
            )
        messages.append(
            {
                "role": "user",
                "content": self.reportMachineConclusionMsg.format(language),
            }
        )

        ret = self.gpt(messages)
        return ret