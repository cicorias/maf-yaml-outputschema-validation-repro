"""Test script to understand how AgentFactory handles outputSchema."""

import asyncio
import os
import tempfile
from pathlib import Path
from xmlrpc import client

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Test YAML with outputSchema
test_yaml = """
kind: prompt
name: test-agent
description: Test agent with outputSchema
instructions: |
  You are a test agent.
  Extract the name and age from the input.
outputSchema:
  properties:
    name:
      kind: string
      description: Person's name
      required: true
    age:
      kind: integer
      description: Person's age
      required: true
    status:
      kind: string
      description: Status indicator
      required: true
      enum:
        - active
        - inactive
"""


async def main():
    """Test AgentFactory with outputSchema."""
    print("=" * 80)
    print("Testing AgentFactory outputSchema handling")
    print("=" * 80)

    # Write test YAML to temp file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(test_yaml)
        yaml_path = f.name

    try:
        # Import and test
        # from agent_framework import ChatAgent, ChatClientProtocol
        # from agent_framework.azure import AzureAIProjectAgentProvider
        from agent_framework_declarative import AgentFactory
        from agent_framework_azure_ai import AzureAIClient
        from azure.identity.aio import DefaultAzureCredential

        # Check if we have required environment variables
        if not os.getenv("AZURE_AI_PROJECT_ENDPOINT") or not os.getenv(
            "AZURE_OPENAI_MODEL"
        ):
            print("ERROR: AZURE_AI_PROJECT_ENDPOINT or AZURE_OPENAI_MODEL not set")
            print("This test requires Azure AI Foundry configuration")
            return

        async with (
            DefaultAzureCredential() as credential,
            AzureAIClient(
                endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
                credential=credential,
                model_deployment_name=os.environ["AZURE_OPENAI_MODEL"],
            ) as client,
        ):
            factory = AgentFactory(
                chat_client=client,
                safe_mode=False,
            )
            print("\n1. Loading agent from YAML...")
            agent = factory.create_agent_from_yaml_path(Path(yaml_path))

            print(f"Created agent: {agent.name}")
            print(f"Agent ID: {agent.id}")

            print("=" * 80)         
            query = "I'm Shawn and 5 years old?"
            print(f"User: {query}")

            print("=" * 80)         
            result = await agent.run(query)
            print(f"Agent: {result}\n")


            print("=" * 80)         
            print("\n2. Agent properties:")
            print(f"   - name: {agent.name}")
            print(f"   - description: {agent.description}")
            print(
                f"   - instructions length: {len(agent.default_options['instructions']) if agent.default_options.get('instructions') else 0}"
            )

            # Check if response_format was set
            print("\n3. Checking ChatAgent attributes:")
            print(f"   - Has __dict__: {hasattr(agent, '__dict__')}")
            if hasattr(agent, "__dict__"):
                print(f"   - Agent.__dict__ keys: {list(agent.__dict__.keys())}")

            # Try to access response_format (if it exists)
            if hasattr(agent, "response_format"):
                print(f"   - response_format: {agent.response_format}")
            else:
                print("   - response_format: NOT SET (attribute doesn't exist)")

            # Check chat_options
            if hasattr(agent, "chat_options"):
                print(f"   - chat_options: {agent.chat_options}")
            else:
                print("   - chat_options: NOT SET")

            # Check if there's any structured output configuration
            if hasattr(agent, "_response_format"):
                print(f"   - _response_format: {agent._response_format}")

            print("\n4. AgentFactory behavior:")
            print("   The AgentFactory loaded the YAML successfully.")
            print(
                "   Need to check if outputSchema is converted to response_format parameter."
            )

    except ImportError as e:
        print(f"\nERROR: Missing import: {e}")
        print("This test requires agent-framework-declarative package")
    except Exception as e:
        print(f"\nERROR: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()
    finally:
        # Cleanup
        if os.path.exists(yaml_path):
            os.unlink(yaml_path)

    print("\n" + "=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
