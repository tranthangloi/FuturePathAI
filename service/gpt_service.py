import openai
from config import OPENAI_API_KEY
from openai.error import (
    AuthenticationError, RateLimitError, APIConnectionError,
    InvalidRequestError, Timeout
)

# Thiết lập API Key
openai.api_key = OPENAI_API_KEY

def suggest_career(mbti, holland, skills, interests):
    """
    Gợi ý nghề nghiệp dựa trên MBTI, Holland, kỹ năng và sở thích.
    """

    prompt = (
        f"MBTI: {mbti}\n"
        f"Holland: {holland}\n"
        f"Kỹ năng: {skills}\n"
        f"Sở thích: {interests}\n"
        "Dựa trên thông tin trên, hãy gợi ý 3 nghề nghiệp phù hợp nhất theo định dạng sau:\n"
        "1. Tên nghề nghiệp\n"
        "- Mô tả ngắn gọn nghề đó\n"
        "- Lý do vì sao phù hợp với người dùng\n"
        "- Những kỹ năng cần thiết cho nghề đó\n\n"
        "Trình bày từng nghề từ 1 đến 3."
    )

    try:
        response = openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-0125:personal::BLkYCPve",
            messages=[
                {"role": "system", "content": "Bạn là một chuyên gia tư vấn hướng nghiệp."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000,
            timeout=15
        )

        choices = response.get("choices", [])
        if not choices or "message" not in choices[0] or "content" not in choices[0]["message"]:
            raise Exception("Không nhận được phản hồi hợp lệ từ GPT.")

        return choices[0]["message"]["content"]

    except AuthenticationError as e:
        raise Exception("❌ Lỗi xác thực API Key. Vui lòng kiểm tra lại.") from e
    except RateLimitError as e:
        raise Exception("⚠️ Đã vượt quá giới hạn gọi API. Vui lòng thử lại sau.") from e
    except APIConnectionError as e:
        raise Exception("🔌 Lỗi kết nối đến OpenAI. Kiểm tra lại mạng.") from e
    except InvalidRequestError as e:
        raise Exception(f"📎 Yêu cầu không hợp lệ: {str(e)}") from e
    except Timeout as e:
        raise Exception("⏱️ Quá thời gian chờ phản hồi từ GPT.") from e
    except Exception as e:
        raise Exception(f"❗ Lỗi không xác định: {str(e)}") from e
