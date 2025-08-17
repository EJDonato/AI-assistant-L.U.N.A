import datetime
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    noise_cancellation,
)
from livekit.plugins import google

from prompts import BASE_INSTRUCTION, GREET_INSTRUCTION
from tools import search_web, check_incoming_schedule, create_event_on_calendar

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=BASE_INSTRUCTION,
            llm=google.beta.realtime.RealtimeModel(
            voice="Leda",
            temperature=1,
        ),
            tools=[
                search_web,
                check_incoming_schedule,
                create_event_on_calendar,
            ]
        )


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            video_enabled=True,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()

    today = datetime.date.today().isoformat()

    await session.generate_reply(
        instructions=f"Today is {today}" + GREET_INSTRUCTION,
    )



if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))