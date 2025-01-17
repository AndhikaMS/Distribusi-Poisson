from flask import Flask, render_template, request
import math
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Fungsi untuk menghitung distribusi Poisson (PMF)
def poisson_pmf(lmbda, k):
    return (math.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)

# Fungsi untuk menghitung distribusi kumulatif Poisson (CDF)
def poisson_cdf(lmbda, k):
    return sum(poisson_pmf(lmbda, i) for i in range(k + 1))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        lmbda = float(request.form["lambda"])  # Parameter rata-rata λ
        k = int(request.form["keberhasilan"])  # Jumlah kejadian yang diinginkan (k)

        # Hitung PMF
        pmf_value = poisson_pmf(lmbda, k)

        # Hitung CDF
        cdf_value = poisson_cdf(lmbda, k)

        # Langkah-langkah PMF
        pmf_steps = {
            "rumus": "P(X = k) = \\frac{e^{-\\lambda} \\cdot \\lambda^k}{k!}",
            "substitusi": f"P(X = {k}) = \\frac{{e^{{-{lmbda:.0f}}} \\cdot {lmbda:.0f}^{{{k}}}}}{{{k}!}}",  # Menggunakan notasi LaTeX untuk pangkat
            "pangkat_lambda": f"{lmbda:.0f}^{{{k}}} = {lmbda ** k:.0f}",  # Menggunakan notasi LaTeX untuk pangkat
            "eksponen": f"e^{{-{lmbda:.0f}}} = {math.exp(-lmbda):.5f}" if math.exp(-lmbda) >= 0.00001 else f"e^{{-{lmbda:.0f}}} = {math.exp(-lmbda):.10f}",  # Menampilkan lebih banyak angka jika kecil
            "faktorial": f"{k}! = {math.factorial(k)}",
            "hasil_akhir": (
                f"P(X = {k}) = \\frac{{{math.exp(-lmbda):.10f} \\cdot {lmbda ** k:.0f}}}{{{math.factorial(k)}}} = {pmf_value:.4f}"  # Menampilkan hasil akhir dengan format yang benar
            )
        }

                # Langkah-langkah untuk menampilkan penjumlahan CDF
        cdf_steps = {
            "rumus": "P(X \leq k) = \sum_{i=0}^{k} P(X = i)",
            "penjumlahan": "P(X \leq k) = P(X = 0) + P(X = 1) + \cdots + P(X = k)"
        }


        # Grafik PMF
        probabilities = [poisson_pmf(lmbda, i) for i in range(k + 10)]
        fig, ax = plt.subplots()
        ax.bar(range(len(probabilities)), probabilities, label="PMF")
        ax.set_xlabel('Jumlah Move (k)')
        ax.set_ylabel('Probabilitas P(X = k)')
        ax.set_title('Distribusi Probabilitas Poisson - PMF')
        plt.legend()

        # Menyimpan grafik ke dalam format gambar
        img_buf = BytesIO()
        plt.savefig(img_buf, format='png')
        img_buf.seek(0)
        img_str = base64.b64encode(img_buf.read()).decode('utf-8')
        img_buf.close()

        # Hitung PMF untuk setiap nilai dari 0 hingga k
        pmf_values = [poisson_pmf(lmbda, i) for i in range(k + 1)]

        # Grafik CDF
        cdf_values = [poisson_cdf(lmbda, i) for i in range(k + 1)]
        fig_cdf, ax_cdf = plt.subplots()
        ax_cdf.plot(range(k + 1), cdf_values, marker='o', label="CDF", color="blue")
        ax_cdf.set_xlabel('Jumlah Move (k)')
        ax_cdf.set_ylabel('Probabilitas P(X ≤ k)')
        ax_cdf.set_title('Distribusi Kumulatif Poisson - CDF')
        plt.legend()

        # Menyimpan grafik CDF ke dalam format gambar
        img_buf_cdf = BytesIO()
        plt.savefig(img_buf_cdf, format='png')
        img_buf_cdf.seek(0)
        img_str_cdf = base64.b64encode(img_buf_cdf.read()).decode('utf-8')
        img_buf_cdf.close()


        # Kirimkan pmf_values ke template
        return render_template(
            "index.html",
            probabilities=probabilities,
            pmf_steps=pmf_steps,
            img_str=img_str,
            img_str_cdf=img_str_cdf,
            lmbda=lmbda,
            k=k,
            pmf_value=pmf_value,
            cdf_value=cdf_value,
            pmf_values=pmf_values  # Menambahkan pmf_values ke template
        )


    return render_template("index.html", probabilities=None, img_str=None, img_str_cdf=None)

if __name__ == "__main__":
    app.run(debug=True)
