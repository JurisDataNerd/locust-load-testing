from locust import HttpUser, task, between
import random

# Daftar Akun MABA Nyata dari user.txt (NIM & Password Tanggal Lahir)
MABA_CREDENTIALS = [
    ("261111001", "26mei2006"),
    ("261111002", "16juli2007"),
    ("261111003", "16juli2004"),
    ("261111004", "5januari2008"),
    ("261111005", "25april2008"),
    ("261111006", "22juni2007"),
    ("261111007", "8januari2005"),
    ("261111008", "31maret2008"),
    ("261111009", "10agustus2007"),
    ("261111010", "8november2007"),
    ("261111011", "7januari2007"),
    ("261111012", "19juli2007"),
    ("261111013", "20juni2008"),
    ("261111014", "30april2008"),
    ("261111015", "28maret2009"),
    ("261111016", "30april2007"),
    ("261111017", "26februari2008"),
    ("261111018", "13september2007"),
    ("261111019", "8maret2008"),
    ("261111020", "20agustus2007"),
    ("261111021", "14februari2007"),
    ("261111022", "20januari2008"),
    ("261111024", "21mei2008"),
    ("261111025", "26juli2007"),
    ("261111026", "5november2007"),
    ("261111027", "26desember2008"),
    ("261111028", "3mei2003"),
    ("261111029", "16maret2008"),
    ("261111030", "18oktober2007"),
    ("261111031", "12oktober2007"),
    ("261111032", "1juli2005"),
    ("261111033", "22februari2008"),
    ("261111034", "10juni2007"),
    ("261111035", "28maret2008"),
    ("261111036", "14desember2007"),
    ("261111037", "17mei2007"),
    ("261111038", "9maret2008"),
    ("261111039", "13juli2008"),
    ("261111040", "28mei2008"),
    ("261111041", "9juni2009"),
    ("261111042", "1mei2007"),
    ("261111043", "28desember2007"),
    ("261111044", "19agustus2007"),
    ("261111045", "1mei2007"),
    ("261111046", "11maret2008"),
    ("261111047", "27agustus2007"),
    ("261111048", "1maret2002"),
    ("261111049", "23agustus2006"),
    ("261111050", "19mei2007"),
]

class MabaUser(HttpUser):
    # Mahasiswa jeda aksi antara 2 sampai 4 detik
    wait_time = between(2, 4)

    def on_start(self):
        """Login menggunakan akun resmi MABA yang valid"""
        nim, password = random.choice(MABA_CREDENTIALS)
        res = self.client.post("/api/auth/login", json={
            "username": nim,
            "password": password
        })
        if res.status_code == 200:
            token = res.json().get("data", {}).get("token")
            self.headers = {"Authorization": f"Bearer {token}"}
        else:
            self.headers = {}

    @task(3)
    def view_dashboard(self):
        """Maba melihat data profil dan tim"""
        self.client.get("/api/auth/me", headers=self.headers)

    @task(5)
    def view_leaderboard(self):
        """Maba memantau papan ranking leaderboard regu"""
        self.client.get("/api/leaderboard", headers=self.headers)

    @task(2)
    def check_ormawa(self):
        """Maba melihat stan expo ormawa"""
        self.client.get("/api/ormawa/booths", headers=self.headers)
