import argparse
import asyncio

import scanner
from config import Config
from obs import OBSClient


async def loop():
    config = Config.load()
    obs_client = await OBSClient.create(**config.client.model_dump())
    if config.profile:
        await obs_client.change_profile(config.profile)
    if config.collection:
        await obs_client.change_collection(config.collection)

    process_to_scene = {}
    scene_to_delay = {}
    for scene_name, scene_params in config.scenes.items():
        if isinstance(scene_params, list):
            scene_params = Config.SceneParams(match=scene_params)
        for process in scene_params.match:
            process_to_scene[process] = scene_name
        scene_to_delay[scene_name] = scene_params.delay

    while True:
        for process in scanner.get_processes():
            if process in process_to_scene:
                scene_name = process_to_scene[process]
                if scene_name == await obs_client.get_scene():
                    break
                print(f"Found {process} -> {scene_name}")
                delay = scene_to_delay[scene_name]
                if delay:
                    print(f"Waiting {delay} seconds")
                    await asyncio.sleep(scene_to_delay[scene_name])
                await obs_client.change_scene(scene_name)
                break
        else:
            if (
                config.default_scene
                and config.default_scene != await obs_client.get_scene()
            ):
                print(f"Changing to default scene {config.default_scene}")
                await obs_client.change_scene(config.default_scene)
        await asyncio.sleep(2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action", choices=["run", "list"], default="run", nargs="?"
    )
    args = parser.parse_args()

    if args.action == "list":
        for process in sorted(scanner.get_processes(), key=str.casefold):
            print(process)
        return

    asyncio.run(loop())


if __name__ == "__main__":
    main()
