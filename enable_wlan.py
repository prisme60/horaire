import lxml.etree
import lxml.html

url = "http://192.168.1.254/cgi/b/_wli_/cfg/?be=0&l0=4&l1=2&name=WLAN:%20montjoie"

def wlan_interface(enableWLAN):
  root = lxml.html.parse(url).getroot()
  #print lxml.etree.tostring(root)
  form_list = root.cssselect("form[name='wlan_intf']")
  form1 = form_list[0]
  #form1.form_values()
  form1.fields['0']='10'
  if(enableWLAN):
    form1.fields['56']='1'  #enable WLAN
  else:
    form1.fields['56']='0'  #disable WLAN
  #form1.form_values()
  lxml.html.submit_form(form1)

def wlan_interface_state():
  root = lxml.html.parse(url).getroot()
  form_list = root.cssselect("form[name='wlan_intf']")
  form1 = form_list[0]
  return form1.fields['56']=='1'


