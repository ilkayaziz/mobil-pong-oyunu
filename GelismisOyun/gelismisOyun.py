import os
import pygame

pygame.init()
GENISLIK, YUKSEKLIK = 600, 400
pencere = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Mobil Uyumlu Pong")

SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KIRMIZI = (255, 0, 0)
YESIL = (0, 255, 0)

raket = pygame.Rect(250, 350, 120, 20)  # Mobilde parmakla tutması kolay olsun diye biraz büyüttük
top = pygame.Rect(290, 190, 15, 15)

top_hiz_x = 4
top_hiz_y = -4
hiz_olcer = pygame.time.Clock()

puan = 0
yuksek_puan = 0
DOSYA_ADI = "yuksek_puan.txt"

if os.path.exists(DOSYA_ADI):
  try:
    with open(DOSYA_ADI, "r") as dosya:
      yuksek_puan = int(dosya.read())
  except:
    yuksek_puan = 0

yazi_tipi = pygame.font.SysFont(None, 30)
buyuk_yazi_tipi = pygame.font.SysFont(None, 60)
oyun_durumu = "menu"

calisiyor = True
while calisiyor:
  for olay in pygame.event.get():
    if olay.type == pygame.QUIT:
      calisiyor = False

    # Menüdeyken ekrana dokunulursa/tıklanırsa oyunu başlat
    if oyun_durumu == "menu" and (olay.type == pygame.MOUSEBUTTONDOWN or olay.type == pygame.KEYDOWN):
      puan = 0
      top.center = (GENISLIK // 2, YUKSEKLIK // 2)
      raket.x = 250
      top_hiz_x = 4
      top_hiz_y = -4
      oyun_durumu = "oyun"

  if oyun_durumu == "oyun":
    # Mobil Dokunma / Fare Kontrolü: Raketin merkezi parmağın X pozisyonuna gelsin
    if pygame.mouse.get_pressed()[0]:  # Ekrana basılı tutuluyorsa
      fare_x, _ = pygame.mouse.get_pos()
      raket.centerx = fare_x

    # Raketin ekran dışına çıkmasını engelle
    if raket.left < 0:
      raket.left = 0
    if raket.right > GENISLIK:
      raket.right = GENISLIK

    # Top Hareketi
    top.x += top_hiz_x
    top.y += top_hiz_y

    if top.left <= 0:
      top.left = 0
      top_hiz_x *= -1
    if top.right >= GENISLIK:
      top.right = GENISLIK
      top_hiz_x *= -1
    if top.top <= 0:
      top.top = 0
      top_hiz_y *= -1

    if top.colliderect(raket):
      top_hiz_y *= -1
      puan += 10
      top.bottom = raket.top

      if puan > yuksek_puan:
        yuksek_puan = puan
        try:
          with open(DOSYA_ADI, "w") as dosya:
            dosya.write(str(yuksek_puan))
        except:
          pass

    if top.top >= YUKSEKLIK:
      oyun_durumu = "menu"

  # Çizimler
  pencere.fill(SIYAH)

  if oyun_durumu == "menu":
    if top.top >= YUKSEKLIK:
      yenildin_metni = buyuk_yazi_tipi.render("OYUN BİTTİ!", True, KIRMIZI)
      pencere.blit(
          yenildin_metni,
          (
              GENISLIK // 2 - yenildin_metni.get_width() // 2,
              YUKSEKLIK // 2 - 80,
          ),
      )
      skor_metni = yazi_tipi.render(f"Toplanan Puan: {puan}", True, BEYAZ)
      pencere.blit(
          skor_metni,
          (
              GENISLIK // 2 - skor_metni.get_width() // 2,
              YUKSEKLIK // 2 - 30,
          ),
      )

    basla_metni = yazi_tipi.render(
        "Başlamak için Ekrana Dokun", True, YESIL
    )
    pencere.blit(
        basla_metni,
        (GENISLIK // 2 - basla_metni.get_width() // 2, YUKSEKLIK // 2 + 20),
    )

    hs_metni = yazi_tipi.render(
        f"En Yüksek Puan (High Score): {yuksek_puan}", True, BEYAZ
    )
    pencere.blit(
        hs_metni,
        (GENISLIK // 2 - hs_metni.get_width() // 2, YUKSEKLIK // 2 + 70),
    )
  else:
    pygame.draw.rect(pencere, BEYAZ, raket)
    pygame.draw.ellipse(pencere, BEYAZ, top)
    puan_gosterge = yazi_tipi.render(f"Puan: {puan}", True, BEYAZ)
    pencere.blit(puan_gosterge, (20, 20))

  pygame.display.flip()
  hiz_olcer.tick(60)

pygame.quit()