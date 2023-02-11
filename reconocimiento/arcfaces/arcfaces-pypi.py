from arcface import ArcFace
face_rec = ArcFace.ArcFace()
emb1 = face_rec.calc_emb("../caras-ejemplo/Richard_Stallman_at_LibrePlanet_2019.jpg")
print(emb1)
# array([-1.70827676e-02, -2.69084200e-02, -5.85994311e-02,  3.33652040e-03,
#         9.58345132e-04,  1.21807214e-02, -6.81217164e-02, -1.33364811e-03,
#        -2.12905575e-02,  1.67165045e-02,  3.52908894e-02, -5.26051633e-02,
# 	   ...
#        -2.11241804e-02,  2.22553015e-02, -5.71946353e-02, -2.33468022e-02],
#       dtype=float32)
emb2 = face_rec.calc_emb("../caras-ejemplo/Richard_M_Stallman_Swathanthra_2014_kerala.jpg")
face_rec.get_distance_embeddings(emb1, emb2)