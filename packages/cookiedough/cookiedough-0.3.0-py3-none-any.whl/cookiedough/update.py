# encoding: utf-8
# api: cookiedough
# type: function
# title: update/scoring
# description: injects sorting parameters in the cookiecutter database entries
# category: init
# version: 0.2
# 
# This is where the dev/ scripts might end up, so that GH/BB/GL could be
# polled from the main window. For now it's just for the scoring algorithm.
# (Basically looks for averages, some benefits for documentation quality.)
#
# 

import re, time, sys

# local settings (not joined with main)
conf = {
    "score.find": "Makefile | NEWS | CHANGES(?:\.md|\.rst)? | \.fpm(?:rc)?",
    "date": time.strftime("%Y-%m-%d"),
}


def f(x, avg=64, min=-0.1):
    """
    That's just an arbitrary inverted cubic function, that happens to provide a neat
    curve mapping ascending towards 1.0, then flattening out again. So we can coalesce
    scoring around an average/preferred value.
    
        |                       f(x) = (6-(x-6)^4/222-x/2)/4
    1.0 |      * * * *  *
        |   *               *   *
    0.5 | *                          *   * 
        |*                                   *    *   
      0 +----------------------------------------------*-----
        0          3                                  10  *
    """
    x = float(x) * 3 / avg 
    x = (6 - (x - 6)**4 / 222 - x / 2) / 4
    return max(x, min)


def non_english(text):
    """ check for any chinese/russian/non-latin glyphs """
    if re.search(r'[\u0370-\u19FF\u3000-\u9fff]{5,}', text, re.U):
        return True
        
def date2float(str):
    """ YYYY-mm-dd to YYYY.mm/12 """
    y,m,*x = str.split("-")
    return int(y) + int(m)/13


def score(d):
    """
    Updates the score{} dict in a template entry (for sorting).
    Only run once on initialization. So, can do a few more checks.
    """
    score = {
        "size": f(d["size"], 64),
        "forks": f(d["size"], 5),
        "stars": f(d["stars"], 20),
        "tickets": f(d["stars"], 10),
        "vars": f(len(d["config"]), 7),
        "readme": f(len(d["readme"]), 2048),
        "files": f(len(d["dir"].split("\n")), 32),
        "lang": -0.9 if non_english(d["readme"]) else 0.0,
        "age": f(date2float(conf["date"]) - date2float(d["updated_at"]), 9/12),
    }

    # custom preferences
    bonus = 0.0
    if r := d["readme"]:
        if r.find("└──") > 0:
            bonus += 0.75
    if c := d["config"]:
        if len(c[0].get("description", "")):
            bonus += 1.25
    if len(d["keywords"]):
        bonus += 0.75
    if d["has_wiki"]:
        bonus += 0.5
    if was_curated(d["name"]):
        bonus += 0.8
    if conf.get("score.find"):
       score["find"] = 0.5 * len(set(re.findall(conf["score.find"], d["dir"]+"\n"+d["readme"], re.X)))
       
    #@todo
    # · points for @example.com
    # · downvotes for `e.g.`
    # · or incomplete url examples

    # combined values
    score["bonus"] = bonus
    score["all"] = sum(score.values())
    d["score"] = score
    #print(d["name"], " =>  ", d["score"]["all"])



def was_curated(name):
    """ previously listed in cookiecutter README """
    ids = ['audreyr/cookiecutter-pypackage', 'wdm0006/cookiecutter-pipproject', 'kragniz/cookiecutter-pypackage-minimal', 'alexkey/cookiecutter-lux-python', 'cookiecutter-flask/cookiecutter-flask',
    'wdm0006/cookiecutter-flask', 'JackStouffer/cookiecutter-Flask-Foundation', 'candidtim/cookiecutter-flask-minimal', 'testdrivenio/cookiecutter-flask-skeleton', 'avelino/cookiecutter-bottle',
    'openstack/cookiecutter', 'sloria/cookiecutter-docopt', 'quokkaproject/cookiecutter-quokka-module', 'hackebrot/cookiecutter-kivy', 'hackebrot/cookiedozer', 'ionelmc/cookiecutter-pylibrary',
    'robinandeer/cookiecutter-pyvanguard', 'beeware/Python-iOS-template', 'beeware/Python-Android-template', 'trytonus/cookiecutter-tryton', 'pytest-dev/cookiecutter-pytest-plugin',
    'tox-dev/cookiecutter-tox-plugin', 'vintasoftware/cookiecutter-tapioca', 'vintasoftware/tapioca-wrapper', 'drgarcia1986/cookiecutter-muffin', 'OctoPrint/cookiecutter-octoprint-plugin',
    'foosel/OctoPrint', 'tokibito/cookiecutter-funkload-friendly', 'tokibito/funkload-friendly', 'mdklatt/cookiecutter-python-app', 'morepath/morepath-cookiecutter', 'Springerle/hovercraft-slides',
    'xguse/cookiecutter-snakemake-analysis-pipeline', 'ivanlyon/cookiecutter-py3tkinter', 'mandeep/cookiecutter-pyqt5', 'aeroaks/cookiecutter-pyqt4', 'conda/cookiecutter-conda-python',
    'mckaymatt/cookiecutter-pypackage-rust-cross-platform-publish', 'Kwpolska/python-project-template', 'AnyBlok/cookiecutter-anyblok-project', 'xuanluong/cookiecutter-python-cli',
    'pydanny/cookiecutter-django', 'agconti/cookiecutter-django-rest', 'marcofucci/cookiecutter-simple-django', 'legios89/django-docker-bootstrap', 'pydanny/cookiecutter-djangopackage',
    'palazzem/cookiecutter-django-cms', 'wildfish/cookiecutter-django-crud', 'lborgav/cookiecutter-django', 'pbacterio/cookiecutter-django-paas', 'jpadilla/cookiecutter-django-rest-framework',
    'dolphinkiss/cookiecutter-django-aws-eb', 'torchbox/cookiecutter-wagtail', 'wagtail/wagtail', 'chrisdev/wagtail-cookiecutter-foundation', 'tkjone/starterkit-django',
    'valerymelou/cookiecutter-django-gulp', 'tkjone/starterkit-wagtail', 'dulacp/cookiecutter-django-herokuapp', 'shenyushun/cookiecutter-simple-django-cn', 'TAMU-CPT/cc-automated-drf-template',
    'Parbhat/cookiecutter-django-foundation', 'pydanny/cookiecutter-django', 'HackSoftware/cookiecutter-django-ansible', 'wemake-services/wemake-django-template',
    'mashrikt/cookiecutter-django-dokku', 'Pylons/pyramid-cookiecutter-alchemy', 'Pylons/pyramid-cookiecutter-starter', 'Pylons/pyramid-cookiecutter-zodb', 'Pylons/substanced-cookiecutter',
    'mikeckennedy/cookiecutter-pyramid-talk-python-starter', 'eviweb/cookiecutter-template', 'retr0h/cookiecutter-molecule', 'iknite/cookiecutter-ansible-role',
    'ferrarimarco/cookiecutter-ansible-role', 'NathanUrwin/cookiecutter-git', 'vincentbernat/bootstrap.c', 'solarnz/cookiecutter-avr', 'Paspartout/BoilerplatePP',
    'SpotlightKid/cookiecutter-dpf-effect', 'SpotlightKid/cookiecutter-dpf-audiotk', '13coders/cookiecutter-kata-gtest', '13coders/cookiecutter-kata-cpputest',
    'SandyChapman/cookiecutter-csharp-objc-binding', 'svetlyak40wt/cookiecutter-cl-project', 'm-x-k/cookiecutter-elm', 'lacion/cookiecutter-golang', 'm-x-k/cookiecutter-java',
    'm-x-k/cookiecutter-spring-boot', 'alexfu/cookiecutter-android', 'agconti/cookiecutter-es6-boilerplate', 'goldhand/cookiecutter-webpack', 'audreyr/cookiecutter-jquery',
    'audreyr/cookiecutter-jswidget', 'audreyr/cookiecutter-component', 'christabor/cookiecutter-tampermonkey', 'ratson/cookiecutter-es6-package', 'matheuspoleza/cookiecutter-angular2',
    'TAMU-CPT/CICADA', 'TAMU-CPT/cc-automated-drf-template', 'thomaslee/cookiecutter-kotlin-gradle', 'larsyencken/pandoc-talk', 'selimb/cookiecutter-latex-article',
    'luismartingil/cookiecutter-beamer', 'JonasGroeger/cookiecutter-mediawiki-extension', 'kkujawinski/cookiecutter-sublime-text-3-plugin', 'fhightower-templates/sublime-snippet-package-template',
    'mahmoudimus/cookiecutter-slim-berkshelf-vagrant', 'audreyr/cookiecutter-complexity', 'keimlink/cookiecutter-reveal.js', 'relekang/cookiecutter-tumblr-theme', 'Plippe/cookiecutter-scala',
    'jpzk/cookiecutter-scala-spark', 'joeyjoejoejr/cookiecutter-atari2600', 'jupyter-widgets/widget-cookiecutter', 'drivendata/cookiecutter-data-science', 'bdcaf/cookiecutter-r-data-analysis',
    'docker-science/cookiecutter-docker-science', 'mkrapp/cookiecutter-reproducible-science', 'jastark/cookiecutter-data-driven-journalism', 'painless-software/painless-continuous-delivery',
    'DualSpark/cookiecutter-tf-module', 'hkage/cookiecutter-tornado', 'Pawamoy/cookiecutter-awesome', 'sindresorhus/awesome', 'bdcaf/cookiecutter_dotfile', 'genzj/cookiecutter-raml']
    return name in ids


# progressbar from rich "▰▰▰▰▰▰▰▰▱▱▱▱▱"
def progress(i=1, n=100, w=72):
    p = i/(n if n else 100)
    s = "▰" * int(round(p * w)) + "▱" * int(round(((1-p) * w)))
    if i >= n:
        print("\033[0K", end="")
    else:
        print("\0337" + s + "\0338", end="")
    sys.stdout.flush()
