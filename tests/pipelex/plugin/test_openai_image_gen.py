import pytest

from pipelex.cogt.exceptions import ImggGenerationError
from pipelex.cogt.llm.llm_models.llm_platform import LLMPlatform
from pipelex.plugin.openai.openai_factory import OpenAIFactory
from pipelex.tools.misc.base_64_utils import save_base64_to_binary_file
from pipelex.tools.misc.file_utils import ensure_path, get_incremental_file_path
from tests.conftest import TEST_OUTPUTS_DIR
from tests.pipelex.test_data import IMGGTestCases


@pytest.mark.imgg
@pytest.mark.inference
@pytest.mark.asyncio(loop_scope="class")
class TestImggByOpenAIGpt:
    @pytest.mark.parametrize("topic, image_desc", IMGGTestCases.IMAGE_DESC)
    async def test_gpt_image_generation(self, topic: str, image_desc: str):
        client = OpenAIFactory.make_openai_client(LLMPlatform.OPENAI)
        result = await client.images.generate(
            prompt=image_desc,
            model="gpt-image-1",
            moderation="low",
            background="transparent",
            quality="low",
            size="1024x1024",
            output_format="png",
            output_compression=100,
            n=2,
        )
        if not result.data:
            raise ImggGenerationError("No result from OpenAI")

        for image_index, image_data in enumerate(result.data):
            image_base64 = image_data.b64_json
            if not image_base64:
                raise ImggGenerationError("No base64 image data received from OpenAI")

            folder_path = f"{TEST_OUTPUTS_DIR}/imgg_by_gpt_image"
            ensure_path(folder_path)
            filename = f"{topic}_{image_index}"
            img_path = get_incremental_file_path(
                base_path=folder_path,
                base_name=filename,
                extension="png",
                avoid_suffix_if_possible=True,
            )
            save_base64_to_binary_file(b64=image_base64, file_path=img_path)
