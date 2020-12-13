from Settings import SETTINGS

if SETTINGS.test is True:
    string = """<link href="http://localhost/api/AgentPeely.ico" rel="icon">"""
    string2 = """<link href="http://localhost/api/css.css" rel="stylesheet">"""
else:
    string = """<link href="https://peely.de/api/AgentPeely.ico" rel="icon">"""
    string2 = """<link href="https://peely.de/api/css.css" rel="stylesheet">"""

header = f"""
<!DOCTYPE html>
<html lang="en">
<head>""" + """
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-167214524-1"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag("js", new Date());

      gtag("config", "UA-167214524-1");
    </script>
    """ + f"""
    
    <meta charset="UTF-8">
    <title>Peely - Dashboard</title>
    <meta content="Peely Discord Bot. Fortnite Discord Bot. Invite me on your Discord Server" name="description">
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <script
      src="https://code.jquery.com/jquery-2.1.4.js"
      integrity="sha256-siFczlgw4jULnUICcdm9gjQPZkw/YPDqhQ9+nAOScE4="
      crossorigin="anonymous">
    </script>
    <meta name="robots" content="index, follow">
    <meta name="keywords" content="Peely, Discord Bot, Discord, Fortnite Bot, Fortnite, Peely Fortnite Bot, Fortnite Bot Peely">
    <meta name="copyright" content="Tamino Seiler">
    <meta name="author" content="Tamino Seiler">
    <meta name="page-topic" content="Discord Bot, Discord, Bot, Peely">
    <meta name="page-type" content="Website">
    <meta name="audience" lang=“en“ content="all">
    <meta content="index,follow" name="robots">
    <meta HTTP-EQUIV="Language" CONTENT="en">
    <meta name="Discord Bot" content="Peely">
    </style>
    <meta HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">
    {string}
    <meta
            content="width=device-width, initial-scale=1.0, maximum-scale=0, user-scalable=0"
            name="viewport"
    />
    {string2}
</head>
<body>""" + """
<div class="loader-wrapper">
  <span class="loader"><span class="loader-inner"></span></span>
</div>
<script>
    $(window).on("load",function(){
      $(".loader-wrapper").fadeOut("slow");
    });
</script>
<script type="text/javascript" src="https://cookiegenerator.eu/cookie.js?position=top&amp;skin=cookielaw1&amp;box_radius=0&amp;animation=shake2&amp;delay=2&amp;bg_color=ffcb2a&amp;msg_color=000000&amp;link_color=00e7ff&amp;msg=We%20use%20cookies%20to%20understand%20how%20you%20use%20our%20site%20and%20to%20improve%20your%20experience.%20This%20includes%20personalizing%20content%20and%20advertising.%20To%20learn%20more%2C%20%5Burl%3Dhttps%3A%2F%2Fcookiegenerator.eu%2Flearnmore%5Dclick%20here%5B%2Furl%5D.%20By%20continuing%20to%20use%20our%20site%2C%20you%20accept%20our%20use%20of%20cookies%2C%20revised%20%5Burl%3Dhttps%3A%2F%2Fpeely.de%2Fprivacy%5DPrivacy%20Policy%5B%2Furl%5D.&amp;accept_background=000000&amp;accept_color=ffa428&amp;accept_radius=100"></script><div class="lol">"""

body = """
</div>
<div class="floatingImpress"><a href="/contact">Contact</a><right>    -    <style>.bmc-button img{height: 34px !important;width: 35px !important;margin-bottom: 1px !important;box-shadow: none !important;border: none !important;vertical-align: middle !important;}.bmc-button{padding: 7px 10px 7px 10px !important;line-height: 35px !important;height:51px !important;min-width:217px !important;text-decoration: none !important;display:inline-flex !important;color:#FFFFFF !important;background-color:#FF813F !important;border-radius: 5px !important;border: 1px solid transparent !important;padding: 7px 10px 7px 10px !important;font-size: 20px !important;letter-spacing:0.6px !important;box-shadow: 0px 1px 2px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 1px 2px 2px rgba(190, 190, 190, 0.5) !important;margin: 0 auto !important;font-family:"Arial", cursive !important;-webkit-box-sizing: border-box !important;box-sizing: border-box !important;-o-transition: 0.3s all linear !important;-webkit-transition: 0.3s all linear !important;-moz-transition: 0.3s all linear !important;-ms-transition: 0.3s all linear !important;transition: 0.3s all linear !important;}.bmc-button:hover, .bmc-button:active, .bmc-button:focus {-webkit-box-shadow: 0px 1px 2px 2px rgba(190, 190, 190, 0.5) !important;text-decoration: none !important;box-shadow: 0px 1px 2px 2px rgba(190, 190, 190, 0.5) !important;opacity: 0.85 !important;color:#FFFFFF !important;}</style><link href="https://fonts.googleapis.com/css?family=Arial" rel="stylesheet"><a class="bmc-button" target="_blank" href="https://www.buymeacoffee.com/peely"><img src="https://cdn.buymeacoffee.com/buttons/bmc-new-btn-logo.svg" alt="Buy me a coffee"><span style="margin-left:15px;font-size:19px !important;">Buy me a coffee</span></a></right></div></div>

</body>
</html>
"""
