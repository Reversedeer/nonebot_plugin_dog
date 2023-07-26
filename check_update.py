import httpx
from .utils import current_version
from .__init__ import check


@check.handle()
async def check_update():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.github.com/repos/Reversedeer/nonebot_plugin_dog/releases/latest')
        data = response.json()
        latest_version = data['info']['version']
        if current_version != latest_version:
            await check.finish((f'=======插件更新=======\nnonebot-plugin-dog\n当前Version: {current_version}\n最新Version: {latest_version}\n======插件可更新======'), block = False)
        else:
            await check.finish((f'=======插件更新=======\nnonebot-plugin-dog\n当前Version：{latest_version}\n======插件已最新======'), block=False)


        