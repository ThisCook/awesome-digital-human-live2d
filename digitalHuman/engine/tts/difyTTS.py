# -*- coding: utf-8 -*-
'''
@File    :   edgeTTS.py
@Author  :   一力辉 
'''

from ..builder import TTSEngines
from ..engineBase import BaseEngine
import httpx
from typing import Optional
from digitalHuman.utils import httpxAsyncClient
from digitalHuman.utils import logger
from digitalHuman.utils import TextMessage, AudioMessage, AudioFormatType
from digitalHuman.utils.audio import mp3ToWav

__all__ = ["DifyAPI"]


@TTSEngines.register("DifyAPI")
class DifyAPI(BaseEngine):
    async def run(self, input: TextMessage, **kwargs) -> Optional[TextMessage]:
        try: 
            API_URL = ""
            API_KEY = ""
            # 参数填充
            for paramter in self.parameters():
                if paramter['NAME'] == "DIFY_API_URL":
                    API_URL = paramter['DEFAULT'] if paramter['NAME'] not in kwargs else kwargs[paramter['NAME']]
                if paramter['NAME'] == "DIFY_API_KEY":
                    API_KEY = paramter['DEFAULT'] if paramter['NAME'] not in kwargs else kwargs[paramter['NAME']]

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {API_KEY}'
            }
            payload = {
                "text": input.data,
                "user": 'adh',
            }

            resp = httpx.post(API_URL + "/text-to-audio", json=payload, headers=headers)

            message = AudioMessage(
                data=mp3ToWav(resp.content),
                desc=input.data,
                format=AudioFormatType.WAV,
                sampleRate=16000,
                sampleWidth=2,
            )
            return message
            
        except Exception as e:
            logger.error(f"[TTS] Engine run failed: {e}", exc_info=True)
            return None