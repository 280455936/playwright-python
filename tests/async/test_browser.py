# Copyright (c) Microsoft Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

import pytest

from playwright import Error
from playwright.async_api import Browser


async def test_should_create_new_page(browser):
    page1 = await browser.newPage()
    assert len(browser.contexts) == 1

    page2 = await browser.newPage()
    assert len(browser.contexts) == 2

    await page1.close()
    assert len(browser.contexts) == 1

    await page2.close()
    assert len(browser.contexts) == 0


async def test_should_throw_upon_second_create_new_page(browser):
    page = await browser.newPage()
    with pytest.raises(Error) as exc:
        await page.context.newPage()
    await page.close()
    assert "Please use browser.newContext()" in exc.value.message


async def test_version_should_work(browser: Browser, is_chromium):
    version = browser.version
    if is_chromium:
        assert re.match(r"^\d+\.\d+\.\d+\.\d+$", version)
    else:
        assert re.match(r"^\d+\.\d+", version)