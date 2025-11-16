from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import noise_cancellation
from livekit.plugins import google
from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION

load_dotenv()


class MediMan(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,  # Medical-focused instruction
            llm=google.beta.realtime.RealtimeModel(
                voice="Aoede",          # Speech output
                temperature=0.6,        # Stable medical tone
            ),
            tools=[],  # ❌ No tools (weather, search, email removed)
        )


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession()

    await session.start(
        room=ctx.room,
        agent=MediMan(),
        room_input_options=RoomInputOptions(
            video_enabled=False,   # No video needed for medical voice assistant
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions=SESSION_INSTRUCTION,
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
