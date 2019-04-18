# -*- coding: utf-8 -*-
import binascii
import json
import base64
import random
from scrapy_splash import SplashRequest
import scrapy


script = """
function main(splash, args)
  splash.images_enabled = false
  splash.response_body_enabled = true
  splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36")
  assert(splash:go(args.url))
  assert(splash:wait(args.wait))
  return splash:har()
end
"""


class DouyinSpider(scrapy.Spider):
    name = "douyin"
    video_url = 'http://i.snssdk.com/video/urls/v/1/toutiao/mp4/{}'

    def start_requests(self):
        data = {"56874100517": "办公室小野"}
        for uid, name in data.items():
            url = "https://www.douyin.com/share/user/"+uid
            yield SplashRequest(url, callback=self.parse,
                                endpoint="execute",
                                args={'lua_source': script, 'wait': 7},
                                meta={"name": name, "uid": uid}
                                )

    def parse(self, response):
        name = response.meta["name"]
        uid = response.meta["uid"]
        res = json.loads(response.text)
        for i in res["log"]["entries"]:
            if "/web/api/v2/aweme/post" not in i["request"]["url"]:
                continue
            text = i["response"]["content"]["text"]
            json_data = base64.b64decode(text.encode("utf-8")).decode("utf-8")
            data = json.loads(json_data)
            for t in data.get("aweme_list", []):
                item = dict()
                item["duration"] = int(t["video"]["duration"] / 1000)
                item["video_id"] = t["aweme_id"]
                item["uid"] = uid
                item["video_desc"] = t["desc"].replace("@抖音小助手", "").replace("抖音", "")
                item["image_url"] = t["video"]["origin_cover"]["url_list"][0]
                item["create_time"] = "2019-04-16 00:00:00"
                item["nickname"] = "抖音-" + name
                uri = t["video"]["play_addr"]["uri"]
                r, s = self.get_vid(uri)
                url = self.video_url.format(uri) + "?r={r}&s={s}".format(r=r, s=s)
                yield scrapy.Request(url, callback=self.detail, meta={"item": item})

    def detail(self, response):
        item = response.meta["item"]
        p = json.loads(response.text)
        a = p['data']['video_list']['video_1']['main_url']
        time = p['data']['video_duration']
        item["video_url"] = bytes.decode(base64.standard_b64decode(a))
        item["duration"] = int(time)
        yield item

    def get_vid(self, vid):
        r = str(random.random())[2:]
        url = self.video_url.format(vid)
        m = url.replace('http://i.snssdk.com', '')
        n = m + '?r=' + r
        n = bytes(n, encoding="utf8")
        c = binascii.crc32(n)
        s = self.right_shift(c, 0)
        return r, s

    @staticmethod
    def right_shift(val, n):
        return val >> n if val >= 0 else (val + 0x100000000) >> n
