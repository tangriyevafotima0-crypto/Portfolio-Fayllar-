"""Streamlit main application for AI Image Generator."""

import streamlit as st
from generator import ImageGenerator, ImageGeneratorError
from config import Config


def main() -> None:
    """Run the Streamlit image generator application."""
    st.set_page_config(
        page_title="AI Image Generator",
        page_icon="🎨",
        layout="wide"
    )

    st.title("🎨 AI Image Generator")
    st.markdown("Generate stunning images from text descriptions using DALL-E.")

    try:
        Config.validate()
        generator = ImageGenerator(api_key=Config.OPENAI_API_KEY)
    except ValueError as e:
        st.error(f"Configuration error: {e}")
        st.info("Please set your OPENAI_API_KEY in the .env file.")
        return

    col1, col2 = st.columns([2, 1])

    with col1:
        prompt = st.text_area(
            "Describe your image:",
            placeholder="A futuristic city at sunset with flying cars...",
            height=100
        )

    with col2:
        size = st.selectbox(
            "Image Size:",
            options=["1024x1024", "1024x1792", "1792x1024"],
            index=0
        )
        quality = st.selectbox(
            "Quality:",
            options=["standard", "hd"],
            index=0
        )

    if st.button("Generate Image", type="primary", use_container_width=True):
        if not prompt.strip():
            st.warning("Please enter a description for your image.")
            return

        with st.spinner("Generating your image..."):
            try:
                image_url = generator.generate_image(
                    prompt=prompt.strip(),
                    size=size
                )
                st.image(image_url, caption=prompt, use_column_width=True)

                st.download_button(
                    label="Download Image URL",
                    data=image_url,
                    file_name="generated_image_url.txt",
                    mime="text/plain"
                )

            except ImageGeneratorError as e:
                st.error(f"Generation failed: {e}")

    st.divider()
    st.subheader("Generation History")

    history = generator.get_history()
    if history:
        for i, entry in enumerate(reversed(history)):
            with st.expander(f"#{len(history) - i}: {entry['prompt'][:60]}..."):
                st.write(f"**Size:** {entry['size']}")
                st.write(f"**Generated:** {entry['timestamp']}")
                st.image(entry["url"], use_column_width=True)
    else:
        st.info("No images generated yet. Enter a prompt and click Generate!")


if __name__ == "__main__":
    main()
