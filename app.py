from flask import Flask,render_template,request,url_for,session,redirect
from bs4 import BeautifulSoup 
import requests
from urllib.parse import urljoin
ses = requests.Session()
ses.headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 12; M2103K19PG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36"
app = Flask(__name__,template_folder="website",static_folder="module")
app.config["SECRET_KEY"] = "imfullstackdeveloper"


@app.route('/',methods=["GET","POST"])
def render():
    return render_template("index.html")

@app.route("/home",methods=["GET","POST"])
def home():
    return render_template("index.html")


@app.route("/about",methods=["GET","POST"])
def about():
    return render_template('about.html')
@app.route("/search",methods=["GET","POST"])
def Search():
    try:
        if request.method == "POST":
            url = "https://search17.lycos.com/web/"
            urls = []
            url_title = []
            results_url = []
            results_desc = []
            q = request.form.get("search")
            resp = ses.get(url,params={"q":q})
            soup = BeautifulSoup(resp.content,"html.parser")
            for result in soup.find_all("li","result-item"):
                for result_title in result.find_all("span","result-url"):
                    results_url.append(result_title.text)

                for desc in result.find_all("span","result-description"):
                    results_desc.append(desc.text)

                links = result.find_all("a")
                for link in links:
                    urls.append(link.attrs.get("href"))
                    url_title.append(link.text)

            # 20 link
            new_url = ""
            for Next in soup.find_all("ul","pagination"):
                for a in Next.find_all("a"):
                    new_url = urljoin(url,a.attrs.get("href"))
            
            resp = ses.get(new_url)
            soup = BeautifulSoup(resp.content,"html.parser")
            for result in soup.find_all("li","result-item"):
                for result_title in result.find_all("span","result-url"):
                    results_url.append(result_title.text)

                for desc in result.find_all("span","result-description"):
                    results_desc.append(desc.text)

                links = result.find_all("a")
                for link in links:
                    urls.append(link.attrs.get("href"))
                    url_title.append(link.text)

            # 30 link
            new_url = ""
            for Next in soup.find_all("ul","pagination"):
                for a in Next.find_all("a"):
                    new_url = urljoin(url,a.attrs.get("href"))
            resp = ses.get(new_url)
            soup = BeautifulSoup(resp.content,"html.parser")
            for result in soup.find_all("li","result-item"):
                for result_title in result.find_all("span","result-url"):
                    results_url.append(result_title.text)

                for desc in result.find_all("span","result-description"):
                    results_desc.append(desc.text)


                links = result.find_all("a")
                for link in links:
                    urls.append(link.attrs.get("href"))
                    url_title.append(link.text)


            # 40 link
            return render_template('search.html',query=q,url=urls,title=url_title,domain=results_url,desc=results_desc)
        return redirect(url_for('home'))

    except requests.ConnectionError:
        return render_template("connectionError.html")


if __name__ == "__main__":
    app.run(debug=True) 
