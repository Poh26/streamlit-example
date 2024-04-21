cat > ~/gemini-app/app_tab3.py <<EOF
 import streamlit as st
 from vertexai.preview.generative_models import GenerativeModel, Part
 from response_utils import *
 import logging

 # merender tab Playground Gambar dengan beberapa tab turunan
 def render_image_playground_tab(multimodal_model_pro: GenerativeModel):

     st.write("Menggunakan Gemini 1.0 Pro Vision - Model multimodal")
     recommendations, screens, diagrams, equations = st.tabs(["Rekomendasi furnitur", "Petunjuk oven", "Diagram ER", "Penalaran matematika"])

     with recommendations:
         room_image_uri = "gs://cloud-training/OCBL447/gemini-app/images/living_room.jpeg"
         chair_1_image_uri = "gs://cloud-training/OCBL447/gemini-app/images/chair1.jpeg"
         chair_2_image_uri = "gs://cloud-training/OCBL447/gemini-app/images/chair2.jpeg"
         chair_3_image_uri = "gs://cloud-training/OCBL447/gemini-app/images/chair3.jpeg"
         chair_4_image_uri = "gs://cloud-training/OCBL447/gemini-app/images/chair4.jpeg"

         room_image_url = "https://storage.googleapis.com/"+room_image_uri.split("gs://")[1]
         chair_1_image_url = "https://storage.googleapis.com/"+chair_1_image_uri.split("gs://")[1]
         chair_2_image_url = "https://storage.googleapis.com/"+chair_2_image_uri.split("gs://")[1]
         chair_3_image_url = "https://storage.googleapis.com/"+chair_3_image_uri.split("gs://")[1]
         chair_4_image_url = "https://storage.googleapis.com/"+chair_4_image_uri.split("gs://")[1]        

         room_image = Part.from_uri(room_image_uri, mime_type="image/jpeg")
         chair_1_image = Part.from_uri(chair_1_image_uri,mime_type="image/jpeg")
         chair_2_image = Part.from_uri(chair_2_image_uri,mime_type="image/jpeg")
         chair_3_image = Part.from_uri(chair_3_image_uri,mime_type="image/jpeg")
         chair_4_image = Part.from_uri(chair_4_image_uri,mime_type="image/jpeg")

         st.image(room_image_url,width=350, caption="Gambar ruang tamu")
         st.image([chair_1_image_url,chair_2_image_url,chair_3_image_url,chair_4_image_url],width=200, caption=["Kursi 1","Kursi 2","Kursi 3","Kursi 4"])

         st.write("Ekspektasi: Rekomendasikan kursi yang dapat melengkapi gambar ruang tamu.")
prompt_list = ["Pertimbangkan kursi berikut:",
                     "chair 1:", chair_1_image,
                     "chair 2:", chair_2_image,
                     "chair 3:", chair_3_image, "and",
                     "chair 4:", chair_4_image, "\n"
                     "Untuk setiap kursi, jelaskan alasan kursi tersebut cocok atau tidak cocok untuk ruangan berikut:",
                     room_image,
                     "Hanya rekomendasikan untuk ruangan yang disediakan, bukan yang lain.
Berikan rekomendasi Anda dalam format tabel beserta nama kursi dan alasannya dalam kolom.",
]

         tab1, tab2 = st.tabs(["Respons", "Prompt"])
         generate_image_description = st.button("Buat rekomendasi", key="generate_image_description")
         with tab1:
             if generate_image_description and prompt_list: 
                 with st.spinner("Membuat rekomendasi menggunakan Gemini..."):
response = get_gemini_pro_vision_response(multimodal_model_pro, prompt_list)
                     st.markdown(response)
                     logging.info(response)
         with tab2:
             st.write("Prompt yang digunakan:")
             st.text(prompt_list)
 EOF
