import inspect

import humps
from simpleobsws import Request, RequestResponse, WebSocketClient


class OBSClient:
    client: WebSocketClient

    def __init__(self):
        # prevent calling directly
        MATCH = "OBSClient.create"
        if inspect.stack()[1].code_context[0].strip().startswith(MATCH):
            raise TypeError(f"OBSClient must be created using {MATCH}")

    @classmethod
    async def create(cls, host="localhost", port=4444, password=""):
        result = cls()
        url = f"ws://{host}:{port}"
        result.client = WebSocketClient(url=url, password=password)
        await result.client.connect()
        await result.client.wait_until_identified()
        if not result.client.is_identified():
            raise ValueError("Failed to authenticate")
        return result

    async def close(self):
        await self.client.disconnect()

    async def call(self, request: str, **params) -> RequestResponse:
        request = Request(
            request, {humps.camelize(k): v for k, v in params.items()}
        )
        print(">", request)
        result = await self.client.call(request)
        print("<", result)
        return result

    async def get_scene(self):
        result = await self.call("GetCurrentProgramScene")
        return result.responseData["currentProgramSceneName"]

    async def change_scene(self, scene_name: str):
        await self.call("SetCurrentProgramScene", scene_name=scene_name)

    async def change_profile(self, profile: str):
        await self.call("SetCurrentProfile", profile_name=profile)

    async def change_collection(self, collection: str):
        await self.call(
            "SetCurrentSceneCollection", scene_collection_name=collection
        )
