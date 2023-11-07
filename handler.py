import runpod
from codeinterpreterapi import CodeInterpreterSession, File
import aiohttp
import base64


async def handler(event):
    data = event['input']

    open_ai_key = data['open_ai_key']
    prompt = data['prompt']
    file_urls = data['file_urls']

    input_files = list()

    if file_urls:
        for file in file_urls:
            async with aiohttp.ClientSession() as session:
                async with session.get(file['url']) as r:
                    input_files.append(File(name=file['file_name']+'.csv', content=await r.read()))

    async with CodeInterpreterSession(model='gpt-3.5-turbo', openai_api_key=open_ai_key) as session:
        response = await session.generate_response(
            prompt,
            files=input_files,
            detailed_error=True
        )

    images = []

    for file in response.files:
        images.append(base64.b64encode(file.content).decode())

    output = {
        "AI": response.content,
        "images": images,
    }

    return output


runpod.serverless.start({"handler": handler})
