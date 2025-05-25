import os
import base64
import zipfile
import random
import string
from io import BytesIO

# Constants
FILE_SIZE_MB = 3
FILE_SIZE_BYTES = FILE_SIZE_MB * 1024 * 1024
FILENAME = "/random_data.txt"

# Helper to generate random data and write to file
def generate_random_file(filename, size_bytes):
    with open(filename, "wb") as f:
        data = os.urandom(size_bytes)
        f.write(data)
    return data

def get_data_from_file(filename):
    with open(filename, "rb") as f:
        data = f.read()
    return data

# Base64 encode and decode
def base64_encode(data):
    return base64.b64encode(data)

def base64_decode(data):
    return base64.b64decode(data)

# Zip compress and decompress
def zip_compress(data, name="data"):
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr(name, data)
    return buffer.getvalue()

def zip_decompress(data, name="data"):
    buffer = BytesIO(data)
    with zipfile.ZipFile(buffer, 'r') as zipf:
        return zipf.read(name)

# Write and test compression ratios
#original_data = generate_random_file(FILENAME, FILE_SIZE_BYTES)

#target_file = './sample_data/california_housing_train.csv'
#original_data = get_data_from_file(target_file)

original_data = """
我想学一个遨游太空的魔法
Wǒ xiǎng xué yīgè áoyóu tàikōng de mófǎ
把所有心愿都在夜空种下
Bǎ suǒyǒu xīnyuàn dōu zài yèkōng zhǒng xià
陪着所有星星在梦里越长越大
Péizhe suǒyǒu xīngxīng zài mèng lǐ yuè zhǎng yuè dà

我想风也不知道它该要去哪
Wǒ xiǎng fēng yě bù zhīdào tā gāi yào qù nǎ
我想落叶也会偷偷想家
Wǒ xiǎng luòyè yě huì tōutōu xiǎng jiā
学会了眼泪当做汗水偷偷地擦
Xuéhuìle yǎnlèi dàngzuò hànshuǐ tōutōu de cā

我会等枯树生出芽开出新的花
Wǒ huì děng kū shùshēng chūyá kāi chū xīn de huā
等着阳光刺破黑暗第一缕朝霞
Děngzhe yángguāng cì pò hēi'àn dì yī lǚ zhāoxiá
我会等一场雨落下把回忆都冲刷
Wǒ huì děng yīchǎng yǔ luòxià bǎ huíyì dōu chōngshuā
再与你一起去看外面世界到底有多大
Zài yǔ nǐ yīqǐ qù kàn wàimiàn shìjiè dàodǐ yǒu duōdà

我会等冬的雪融化蒲扇里的夏
Wǒ huì děng dōng de xuě rónghuà púshàn lǐ de xià
守着深夜里的星星眨眼不说话
Shǒuzhe shēnyè lǐ de xīngxīng zhǎyǎn bù shuōhuà
我会等故事里的你再给我讲笑话
Wǒ huì děng gùshì lǐ de nǐ zài gěi wǒ jiǎng xiàohuà
相信美梦和你 总有一天会预先到达
Xiāngxìn měimèng hé nǐ zǒng yǒu yītiān huì yùxiān dàodá
    """
original_data = original_data.encode()

original_size = len(original_data)

# Base64 only
b64_data = base64_encode(original_data)
b64_size = len(b64_data)
b64_decoded = base64_decode(b64_data)
assert original_data == b64_decoded

# Zip only
zip_data = zip_compress(original_data)
zip_size = len(zip_data)
zip_decoded = zip_decompress(zip_data)
assert original_data == zip_decoded

# Base64 then Zip
b64_then_zip = zip_compress(b64_data)
b64_then_zip_size = len(b64_then_zip)
b64_then_zip_decoded = base64_decode(zip_decompress(b64_then_zip))
assert original_data == b64_then_zip_decoded

# Zip then Base64
zip_then_b64 = base64_encode(zip_data)
zip_then_b64_size = len(zip_then_b64)
zip_then_b64_decoded = zip_decompress(base64_decode(zip_then_b64))
assert original_data == zip_then_b64_decoded

# Return all sizes and ratios
resultant = {
    "original_size": original_size,

    "base64_size": b64_size,
    "base64_ratio": b64_size / original_size,

    "zip_size": zip_size,
    "zip_ratio": zip_size / original_size,

    "b64_then_zip_size": b64_then_zip_size,
    "b64_then_zip_ratio": b64_then_zip_size / original_size,

    "zip_then_b64_size": zip_then_b64_size,
    "zip_then_b64_ratio": zip_then_b64_size / original_size
}

import json
print(json.dumps(resultant, indent=4))

# get minimal compression ratio
ratios = {k: v for k, v in resultant.items() if 'ratio' in k}
min_ratio_key = min(ratios, key=ratios.get)
min_ratio_value = ratios[min_ratio_key]

print(f"Best compression method: {min_ratio_key} with ratio {min_ratio_value:.4f}")

# Extract only the compression ratios
ratios = {k: v for k, v in resultant.items() if 'ratio' in k}

# Sort by ratio (ascending: smaller is better)
sorted_ratios = sorted(ratios.items(), key=lambda item: item[1])

# Print ranked list
print("Compression methods ranked by efficiency (best to worst):")
for i, (method, ratio) in enumerate(sorted_ratios, start=1):
    print(f"{i}. {method:<25} - Ratio: {ratio:.4f}")

# Best method
best_method, best_ratio = sorted_ratios[0]
print(f"\n🏆 Best compression method: {best_method} with ratio {best_ratio:.4f}")

"""
{
    "original_size": 1419,
    "base64_size": 1892,
    "base64_ratio": 1.3333333333333333,
    "zip_size": 1027,
    "zip_ratio": 0.7237491190979564,
    "b64_then_zip_size": 1307,
    "b64_then_zip_ratio": 0.9210711768851304,
    "zip_then_b64_size": 1372,
    "zip_then_b64_ratio": 0.966878083157153
}
Best compression method: zip_ratio with ratio 0.7237
Compression methods ranked by efficiency (best to worst):
1. zip_ratio                 - Ratio: 0.7237
2. b64_then_zip_ratio        - Ratio: 0.9211
3. zip_then_b64_ratio        - Ratio: 0.9669
4. base64_ratio              - Ratio: 1.3333

🏆 Best compression method: zip_ratio with ratio 0.7237
"""