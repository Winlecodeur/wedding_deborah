from django.db import models
from django.utils import timezone
from PIL import Image,ImageDraw,ImageFont
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
import os
from django.core.exceptions import ValidationError
#here's a way to add a table
class Table(models.Model):
    name = models.CharField(max_length=150, unique=True)
    number = models.PositiveBigIntegerField(default="", unique=True)
    capacite = models.PositiveIntegerField(default=0)
    created_at  = models.DateTimeField(default=timezone.now)

    def capacity(self):
        opacity = self.tables.count()
        if self.pk and  opacity >= self.capacite :
            raise ValidationError(f"La table '{self.name}' est déjà pleine et ne peut plus accueillir de nouvelles personnes.")
        
    def save(self, *args, **kwargs):
        """Vérifie la capacité avant d'enregistrer."""
        super().save(*args, **kwargs)
        self.capacity()
        super().save(*args, **kwargs)

    def __str__(self):
        return f" {self.name} {self.number}  "

class Invite(models.Model):
    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    whatsapp_num = models.CharField(max_length=20)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="tables")
    photo = models.ImageField(upload_to='photos_invites/', blank=True, null=True, default='photos/wedding inv debo code QR 004 11 1 1 1 1.jpg')  # Photo par défaut
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)  # QR code associé à chaque invité
    is_scan = models.BooleanField(default=False)  # Si l'invité a été scanné if the user was successfull scanned 
    created_at = models.DateTimeField(default=timezone.now)
    is_sent  =models.BooleanField(default=False)
    statut_choices = [
           ('COUPLE' , 'couple'),
        ('MR' , 'mr'),
           ('MADAME','madame')
    ]
    statut = models.CharField(max_length=11, choices=statut_choices, default='COUPLE')
    guest_count = models.PositiveBigIntegerField(default=1)
    def clean(self):
        """Empêche d'ajouter une réservation si cela dépasse la capacité de la table."""
        existing_reservations = self.table.tables.exclude(pk=self.pk)
        total_guests = sum(res.guest_count for res in existing_reservations)  
        if total_guests + self.guest_count > self.table.capacite:
            raise ValidationError(f"La table '{self.table.name}' ne peut pas accueillir {self.guest_count} personnes de plus.")
    def save(self, *args, **kwargs):
        # Première sauvegarde pour obtenir un ID
        if not self.id:
            super().save(*args, **kwargs)  # Sauvegarde initiale pour générer un ID
        if not self.clean : 
            super().save(*args, **kwargs)
        # Génération automatique du QR code unique pour chaque invité
        if not self.qr_code:
            qr_image = self.generate_custom_qr_code(f"http://127.0.0.1:8000/{self.id}")  # Lien vers la page d'invité spécifique
            self.qr_code.save(f'qr_{self.id}.png', qr_image, save=False)
        super().save(*args, **kwargs)

    def generate_custom_qr_code(self, data):

        qr = qrcode.QRCode(
            version=1,  # Taille du QR code, plus le numéro est élevé, plus le QR code est grand
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Taux d'erreur permis
        box_size=5,  # Taille de chaque "boîte" dans le QR code
        border=4,  # Largeur de la bordure du QR code
    )

        qr.add_data(data)  # Ajoute les données (URL, texte, etc.)
        qr.make(fit=True)

    # Personnalise la couleur du QR code
        qr_img = qr.make_image(fill_color=(184,140,6), eye_color='black',back_color='white' ).convert("RGBA")

    # Charger l'image par défaut de l'invité
        photo_path = os.path.join(settings.MEDIA_ROOT, 'photos/wedding inv debo code QR 004 11 1 1 1 1.jpg')  # Photo par défaut
        photo = Image.open(photo_path)

    # Redimensionner le QR code
        qr_size = (300, 300)
        qr_img = qr_img.resize(qr_size)

    # Superposer le QR code sur la photo (ici en bas à droite)
        position = ((photo.width - qr_img.width) // 2 + 40, (photo.height - qr_img.height) // 2 + 560)
        photo.paste(qr_img, position)
         # Ajouter le nom de l'invité au-dessus du QR code
        draw = ImageDraw.Draw(photo)
        try:
            font = ImageFont.truetype("arial.ttf", 21)  # Police Arial, taille 40
        except:
            font = ImageFont.load_default()
        text =   self.name  # Nom de l'invité

    # Calculer la largeur du texte
        text_width = font.getlength(text)  # Largeur du texte en pixels

    # Calculer la position x pour centrer le texte
        qr_center_x = position[0] + (qr_img.width // 2)  # Centre horizontal du QR code
        text_x = qr_center_x - (text_width // 2 - 10)  # Position x pour centrer le texte

    # Définir la position du texte
        text_position = (text_x, position[1] - 45)  # Ajustez la valeur y pour la position verticale

    # Dessiner le texte
        draw.text(text_position, text, font=font, fill=(184,140,6))  
        
    # Sauvegarder l'image combinée dans un buffer
        img_byte_arr = BytesIO()
        photo.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

    # Créer un fichier Django ImageFile et le sauvegarder
        self.qr_code.save(f'qr_invite_{self.id}.png', ContentFile(img_byte_arr.getvalue()), save=False)
        self.save()  # Sauvegarder l'image dans le modèle
        
    # Retourner le fichier image pour une utilisation ultérieure
        return ContentFile(img_byte_arr.getvalue(), name='custom_qr.png')     # Crée un QR code avec les paramètres de base
    

    def __str__(self):
        return f"{self.name} {self.first_name}"

class Oath(models.Model):
    invite = models.ForeignKey(Invite, related_name='oaths', on_delete=models.CASCADE, null=True)
    created_at =  models.DateTimeField(default=timezone.now)
    text = models.TextField()

    def __str__(self):
        return f"  {self.invite.name} {self.invite.first_name} {self.invite.whatsapp_num}  {self.created_at} {self.text} "