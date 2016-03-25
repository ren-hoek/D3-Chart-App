from flask import Flask, render_template, request
from forms import SelectionForm, AnnualForm
import json

app = Flask(__name__)

#Needs setting as CSRF_ENABLED=True for flask-wtf. Keep secret_key, secret
app.secret_key = ''

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/table', methods=['GET', 'POST'])
def table():
    with open ('results.json','r') as json_file:
        lfs_data = json.load(json_file)

    form = SelectionForm()

    if request.method == 'POST':
        yr=form.year_drop.data
        cond_type=int(form.type_drop.data)
    else:
        form.year_drop.data="2014/15"
        yr="2014/15"
        cond_type=0

    ty = lfs_data["category"][0]["average"][0]["results"][cond_type]["label"]
    cond_values = lfs_data["category"][0]["average"][0]["results"][cond_type]["values"]
    cond_label = lfs_data["category"][0]["average"][0]["results"]

    lab = []
    cd = []
    est = []
    cil = []
    ciu = []
    rt_est = []
    rt_cil = []
    rt_ciu = []

    form.year_drop.choices = (
        [(e["year"],e["year"]) for e in cond_values]
    )

    form.type_drop.choices = (
        [(i-1,e["label"]) for i, e in enumerate(cond_label,1)]
    )

    for ind in lfs_data["category"]:

        label = ind["label"]
        code = ind["code"]

        for row in ind["average"][0]["results"][cond_type]["values"]:
            if row["year"]==yr:
                cd.append(code)
                lab.append(label)
                est.append(row["estimate"][0]["central"])
                cil.append(row["estimate"][0]["cil"])
                ciu.append(row["estimate"][0]["ciu"])
                rt_est.append(row["rate"][0]["central"])
                rt_cil.append(row["rate"][0]["cil"])
                rt_ciu.append(row["rate"][0]["ciu"])

    res = zip(lab,cd,est,cil,ciu,rt_est,rt_cil,rt_ciu)

    return render_template('table.html'
     ,results=res
     ,year=yr
     ,inj_ill_type=ty
     ,form=form)

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    with open ('lfs_ind_est_rnd.json','r') as json_file:
        lfs_data = json.load(json_file)

    form = AnnualForm()

    if request.method == 'POST':
        ind=int(form.ind_drop.data)
        cond_type=int(form.type_drop.data)
    else:
        ind=0
        cond_type=0

    industry = lfs_data["category"]
    cond_label = lfs_data["category"][0]["average"][0]["results"]

    form.ind_drop.choices = (
        [(i-1,e["label"]) for i,e in enumerate(industry,1)]
    )

    form.type_drop.choices = (
        [(i-1,e["label"]) for i, e in enumerate(cond_label,1)]
    )

    form.meas_drop.choices = (
        [(0, "Estimate"), (1, "Rate")]
    )

    cond_values = lfs_data["category"][ind]["average"][0]["results"][cond_type]["values"]

    yr = []
    est = []
    cil = []
    ciu = []
    rt_est = []
    rt_cil = []
    rt_ciu = []

    for row in cond_values:
        yr.append(row["year"])
        est.append(row["estimate"][0]["central"])
        cil.append(row["estimate"][0]["cil"])
        ciu.append(row["estimate"][0]["ciu"])
        rt_est.append(row["rate"][0]["central"])
        rt_cil.append(row["rate"][0]["cil"])
        rt_ciu.append(row["rate"][0]["ciu"])

    res = zip(yr,est,cil,ciu,rt_est,rt_cil,rt_ciu)

    return render_template('graph.html', form=form, results=res)

if __name__ == '__main__':
    app.run(debug=True)
