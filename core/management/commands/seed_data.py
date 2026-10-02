
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Area, Curso, PerfilUsuario

class Command(BaseCommand):
    help = "Limpia y puebla la base de datos con las 7 categorías, 3 carreras y 2 cursos relámpagos por cada una (Total 35)."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Limpiando datos..."))
        Curso.objects.all().delete()
        Area.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        # 1. Crear Coordinador de Prueba
        admin_user = User.objects.create_user('coordinador', 'admin@ticketrb.cl', 'admin123')
        # La señal crea el perfil automáticamente con rol ESTUDIANTE. Lo actualizamos a COORDINADOR.
        admin_user.perfil.rol = 'COORDINADOR'
        admin_user.perfil.save()
        
        # 2. Categorías
        nombres_areas = [
            "Data", 
            "Diseño UX/UI", 
            "Inteligencia Artificial", 
            "Marketing Digital", 
            "Negocios", 
            "Producto", 
            "Programación y Desarrollo"
        ]
        
        areas = {}
        for n in nombres_areas:
            areas[n] = Area.objects.create(nombre=n)
        
        self.stdout.write(self.style.SUCCESS(f"{len(areas)} Áreas creadas."))

        # 3. Poblamiento de Cursos
        # 7 áreas * (3 Carreras + 2 Relámpagos) = 35 cursos
        
        cursos_data = [
            # Data
            {"area": "Data", "tipo": "CARRERA", "titulo": "Data Science Bootcamp", "precio": 1500000, "desc": 20, "img": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=500&q=60"},
            {"area": "Data", "tipo": "CARRERA", "titulo": "Data Analytics Advanced", "precio": 1200000, "desc": 15, "img": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=500&q=60"},
            {"area": "Data", "tipo": "CARRERA", "titulo": "Data Engineering en Cloud", "precio": 1600000, "desc": 25, "img": "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?auto=format&fit=crop&w=500&q=60"},
            {"area": "Data", "tipo": "RELAMPAGO", "titulo": "SQL para Principiantes", "precio": 45000, "desc": 50, "horas": 4, "img": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=500&q=60"},
            {"area": "Data", "tipo": "RELAMPAGO", "titulo": "PowerBI Express", "precio": 50000, "desc": 70, "horas": 6, "img": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=500&q=60"},
            
            # Diseño UX/UI
            {"area": "Diseño UX/UI", "tipo": "CARRERA", "titulo": "Carrera Diseño UX/UI", "precio": 1300000, "desc": 30, "img": "https://images.unsplash.com/photo-1561070791-2526d30994b5?auto=format&fit=crop&w=500&q=60"},
            {"area": "Diseño UX/UI", "tipo": "CARRERA", "titulo": "Product Design", "precio": 1400000, "desc": 20, "img": "https://images.unsplash.com/photo-1586717791821-3f44a563fa4c?auto=format&fit=crop&w=500&q=60"},
            {"area": "Diseño UX/UI", "tipo": "CARRERA", "titulo": "UI Engineering", "precio": 1100000, "desc": 10, "img": "https://images.unsplash.com/photo-1618761714954-0b8cd0026356?auto=format&fit=crop&w=500&q=60"},
            {"area": "Diseño UX/UI", "tipo": "RELAMPAGO", "titulo": "Figma Masterclass", "precio": 35000, "desc": 40, "horas": 3, "img": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?auto=format&fit=crop&w=500&q=60"},
            {"area": "Diseño UX/UI", "tipo": "RELAMPAGO", "titulo": "Microinteracciones con Framer", "precio": 40000, "desc": 50, "horas": 4, "img": "https://images.unsplash.com/photo-1626785774573-4b799315345d?auto=format&fit=crop&w=500&q=60"},
            
            # Inteligencia Artificial
            {"area": "Inteligencia Artificial", "tipo": "CARRERA", "titulo": "Machine Learning Engineer", "precio": 1800000, "desc": 20, "img": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=500&q=60"},
            {"area": "Inteligencia Artificial", "tipo": "CARRERA", "titulo": "AI for Business", "precio": 1500000, "desc": 15, "img": "https://images.unsplash.com/photo-1678120000676-47b192ea60c9?auto=format&fit=crop&w=500&q=60"},
            {"area": "Inteligencia Artificial", "tipo": "CARRERA", "titulo": "Deep Learning Bootcamp", "precio": 1900000, "desc": 30, "img": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=500&q=60"},
            {"area": "Inteligencia Artificial", "tipo": "RELAMPAGO", "titulo": "Prompt Engineering Avanzado", "precio": 25000, "desc": 60, "horas": 2, "img": "https://images.unsplash.com/photo-1678911820864-e2c567c655d7?auto=format&fit=crop&w=500&q=60"},
            {"area": "Inteligencia Artificial", "tipo": "RELAMPAGO", "titulo": "Chatbots con LangChain", "precio": 55000, "desc": 40, "horas": 5, "img": "https://images.unsplash.com/photo-1679083216051-aa510a1a2c0e?auto=format&fit=crop&w=500&q=60"},
            
            # Marketing Digital
            {"area": "Marketing Digital", "tipo": "CARRERA", "titulo": "Growth Marketing", "precio": 1200000, "desc": 40, "img": "https://images.unsplash.com/photo-1432888498266-38ffec3eaf0a?auto=format&fit=crop&w=500&q=60"},
            {"area": "Marketing Digital", "tipo": "CARRERA", "titulo": "Performance Marketing", "precio": 1100000, "desc": 20, "img": "https://images.unsplash.com/photo-1533750349088-cd871a92f312?auto=format&fit=crop&w=500&q=60"},
            {"area": "Marketing Digital", "tipo": "CARRERA", "titulo": "Content Manager", "precio": 900000, "desc": 15, "img": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=500&q=60"},
            {"area": "Marketing Digital", "tipo": "RELAMPAGO", "titulo": "TikTok Ads", "precio": 30000, "desc": 70, "horas": 3, "img": "https://images.unsplash.com/photo-1611162616475-46b635cb6868?auto=format&fit=crop&w=500&q=60"},
            {"area": "Marketing Digital", "tipo": "RELAMPAGO", "titulo": "SEO Técnico Express", "precio": 45000, "desc": 50, "horas": 4, "img": "https://images.unsplash.com/photo-1562577309-4932fdd64cd1?auto=format&fit=crop&w=500&q=60"},
            
            # Negocios
            {"area": "Negocios", "tipo": "CARRERA", "titulo": "Business Analytics", "precio": 1400000, "desc": 25, "img": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=500&q=60"},
            {"area": "Negocios", "tipo": "CARRERA", "titulo": "Emprendimiento Digital", "precio": 1000000, "desc": 10, "img": "https://images.unsplash.com/photo-1556761175-5973dc0f32d7?auto=format&fit=crop&w=500&q=60"},
            {"area": "Negocios", "tipo": "CARRERA", "titulo": "Finanzas Corporativas", "precio": 1600000, "desc": 20, "img": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=500&q=60"},
            {"area": "Negocios", "tipo": "RELAMPAGO", "titulo": "OKRs para Startups", "precio": 40000, "desc": 30, "horas": 3, "img": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=500&q=60"},
            {"area": "Negocios", "tipo": "RELAMPAGO", "titulo": "Negociación Estratégica", "precio": 35000, "desc": 50, "horas": 2, "img": "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=500&q=60"},
            
            # Producto
            {"area": "Producto", "tipo": "CARRERA", "titulo": "Product Management", "precio": 1500000, "desc": 30, "img": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=500&q=60"},
            {"area": "Producto", "tipo": "CARRERA", "titulo": "Scrum Master", "precio": 1100000, "desc": 15, "img": "https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=500&q=60"},
            {"area": "Producto", "tipo": "CARRERA", "titulo": "Agile Coach Bootcamp", "precio": 1600000, "desc": 20, "img": "https://images.unsplash.com/photo-1517048676732-d65bc937f952?auto=format&fit=crop&w=500&q=60"},
            {"area": "Producto", "tipo": "RELAMPAGO", "titulo": "Roadmapping Efectivo", "precio": 30000, "desc": 40, "horas": 2, "img": "https://images.unsplash.com/photo-1542626991-cbc4e32524cc?auto=format&fit=crop&w=500&q=60"},
            {"area": "Producto", "tipo": "RELAMPAGO", "titulo": "User Research Express", "precio": 45000, "desc": 60, "horas": 4, "img": "https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=500&q=60"},
            
            # Programación y Desarrollo
            {"area": "Programación y Desarrollo", "tipo": "CARRERA", "titulo": "Full Stack Web Bootcamp", "precio": 1900000, "desc": 70, "img": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=500&q=60"},
            {"area": "Programación y Desarrollo", "tipo": "CARRERA", "titulo": "Backend Developer con Python", "precio": 1400000, "desc": 30, "img": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?auto=format&fit=crop&w=500&q=60"},
            {"area": "Programación y Desarrollo", "tipo": "CARRERA", "titulo": "Mobile App Development", "precio": 1600000, "desc": 20, "img": "https://images.unsplash.com/photo-1551650975-87deedd944c3?auto=format&fit=crop&w=500&q=60"},
            {"area": "Programación y Desarrollo", "tipo": "RELAMPAGO", "titulo": "Git y GitHub Master", "precio": 20000, "desc": 50, "horas": 2, "img": "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?auto=format&fit=crop&w=500&q=60"},
            {"area": "Programación y Desarrollo", "tipo": "RELAMPAGO", "titulo": "Docker Express", "precio": 45000, "desc": 40, "horas": 4, "img": "https://images.unsplash.com/photo-1605379399642-870262d3d051?auto=format&fit=crop&w=500&q=60"},
        ]
        
        for c_data in cursos_data:
            kwargs = {
                "titulo": c_data["titulo"],
                "descripcion": "Descripción detallada del curso. Aprenderás herramientas clave demandadas en el mercado con profesores expertos.",
                "area": areas[c_data["area"]],
                "tipo": c_data["tipo"],
                "precio_original": c_data["precio"],
                "descuento_porcentaje": c_data["desc"],
                "cupos_totales": 50,
                "cupos_disponibles": 50,
                "imagen_url": c_data["img"]
            }
            if c_data["tipo"] == "CARRERA":
                kwargs["nivel"] = "Principiante a Avanzado"
                kwargs["semanas_duracion"] = 24
                kwargs["cantidad_cursos"] = 4
            else:
                kwargs["duracion_horas"] = c_data["horas"]
                
            Curso.objects.create(**kwargs)
            
        self.stdout.write(self.style.SUCCESS(f"¡Base de datos poblada con {Curso.objects.count()} cursos!"))
        self.stdout.write(self.style.SUCCESS("Usuario Admin: coordinador | Contraseña: admin123"))
