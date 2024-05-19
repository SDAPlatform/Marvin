import json
import os.path
import datetime
from typing import Any, Optional

from phi.tools.toolkit import Toolkit
from phi.tools import Toolkit

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class MarvinCalender(Toolkit):
    def __init__(
        self,
        fixed_max_results: Optional[int] = None,
        headers: Optional[Any] = None,
        proxy: Optional[str] = None,
        proxies: Optional[Any] = None,
        timeout: Optional[int] = 10,
    ):
        super().__init__(name="MarvinCalender")
        self.knowledge_base: Optional[MarvinCalender]
        self.headers: Optional[Any] = headers
        self.proxy: Optional[str] = proxy
        self.proxies: Optional[Any] = proxies
        self.timeout: Optional[int] = timeout
        self.fixed_max_results: Optional[int] = fixed_max_results
        self.register(self.fetch_calender_events)


    def fetch_calender_events(self, minDatetime: str ,  maxDatetime: str) -> str:
        """Use this to fetch calender events for user after a min time and before a max time
        Args:
            minDatetime(str): the min time to fetch the calender events  in YYYY-MM-DD HH:MM:SS.microseconds format.
            maxDatetime(str): the max time to fetch the calender events  in YYYY-MM-DD HH:MM:SS.microseconds format.

        Returns:
            the event or events in this format :  event["start"].get("dateTime", event["start"].get("date")) event["summary"] in a json
        """

        parsed_datetime_min = datetime.strptime(minDatetime, '%Y-%m-%d %H:%M:%S.%f')
        parsed_datetime_max = datetime.strptime(maxDatetime, '%Y-%m-%d %H:%M:%S.%f')


        SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open("token.json", "w") as token:
                    token.write(creds.to_json())

            try:
                service = build("calendar", "v3", credentials=creds)
                # Call the Calendar API
                min = parsed_datetime_min.isoformat() + "Z"  # 'Z' indicates UTC time
                max = parsed_datetime_max.isoformat() + "Z"  # 'Z' indicates UTC time

                print("Getting the upcoming 10 events")
                events_result = (
                    service.events()
                    .list(
                        calendarId="primary",
                        timeMax=max,
                        timeMin=min,
                        maxResults=20,
                        singleEvents=True,
                        orderBy="startTime",
                    )
                    .execute()
                )
                events = events_result.get("items", [])
                if not events:
                    print("No upcoming events found.")
                    return
                
                result = ""
                # Prints the start and name of the next 10 events
                for event in events:
                    start = event["start"].get("dateTime", event["start"].get("date"))
                    result += start + event["summary"] + "\n"

            except HttpError as error:
                print(f"An error occurred: {error}")
        test = json.dumps(result,ensure_ascii = False, indent=2)
        return json.dumps(result, ensure_ascii = False,indent=2)
