import pygame
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
from src.componentes.botao import Botao
import pylab 
from src.db.supabase_class import SupabaseClient


class ProgressoTela:
    def __init__(self, screen, id_usuario):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font_path = "src/fonts/Grand9K Pixel.ttf"
        self.id_usuario = id_usuario
        
        try:
            self.font = pygame.font.Font(self.font_path, 30)
        except Exception:
            self.font = pygame.font.SysFont(None, 30)
    
    def progresso_matplotlib(self, progresso):

        fig = pylab.figure(figsize=[8, 5], dpi=100)
        ax = fig.gca()

        categorias = ["Variáveis", "Estruturas Condicionais", "Laços de Repetição", "Vetores"]

        
        ax.bar(categorias, progresso, color=['blue', 'orange', 'green', 'red'])
        ax.set_ylim(0, 5)
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)
        
        try:
            prop = matplotlib.font_manager.FontProperties(fname=self.font_path)
        
            for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                         ax.get_xticklabels() + ax.get_yticklabels()):
                item.set_fontproperties(prop)
            
            
        except Exception:
            pass
        
        for i, v in enumerate(progresso):
            ax.text(i, v + 0.1, str(v), ha='center', fontsize=10)
        
     
        ax.set_title("Progresso do Usuário", fontsize=16)
        ax.set_ylabel("Número de Questões Resolvidas", fontsize=14)
        ax.set_xlabel("Tópicos", fontsize=14)
    
        pylab.tight_layout()
        
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_argb()
        size = canvas.get_width_height()
        surf = pygame.image.fromstring(raw_data, size, "ARGB")
        return surf
    
    def get_progresso_usuario(self):
        supabase = SupabaseClient()
        progresso = supabase.client.table("resultados").select("*").eq("id_aluno", self.id_usuario).execute()
        if progresso.data == []:
            supabase.client.table("resultados").insert({"id_aluno": self.id_usuario, "score_1": 0, "score_2": 0, "score_3": 0, "score_4": 0}).execute()
            return [0, 0, 0, 0]
        else:
            dados = progresso.data
            return [dados[0]['score_1'], dados[0]['score_2'], dados[0]['score_3'], dados[0]['score_4']]
    
    def mostrar_progresso(self):
        self.screen.fill((252, 255, 217))
        get_progresso = self.get_progresso_usuario()
        progresso_surf = self.progresso_matplotlib(get_progresso)
        

        self.logo_img = pygame.image.load("src/img/logo.png")
        self.logo_img = pygame.transform.scale(self.logo_img, (self.logo_img.get_width() // 2, self.logo_img.get_height() // 2))
        logo_rect = self.logo_img.get_rect(center=(500, 80))
        self.screen.blit(self.logo_img, logo_rect)

        progresso_rect = progresso_surf.get_rect(center=(500, 400))

       
        botao_verde = pygame.image.load("src/img/botao/botao_verde.png").convert_alpha()
        botao_voltar = Botao( x=30, y=30, imagem=botao_verde, text="<--", escala=0.2)
        
    
    
        self.screen.blit(progresso_surf, progresso_rect)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit("Usuário saiu do jogo.")
            if botao_voltar.draw(self.screen):
                return False
            pygame.display.flip()