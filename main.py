import requests
import json
from concurrent.futures import ThreadPoolExecutor

def check_email(email, headers, payload_template):
    payload = payload_template.copy()
    payload["username"] = email

    response = requests.post("https://login.microsoftonline.com/common/GetCredentialType?mkt=fr", headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        print(f"{email} => {str(data.get('IfExistsResult'))}")
        # Check the result of the API call
        if data.get("IfExistsResult") != 1:
            with open('valide.txt', 'a') as file:
                file.write(email + "\n")
        else:
            with open('invalid.txt', 'a') as file:
                file.write(email + "\n")
    else:
        print(f"Error: Could not process {email}")

def check_emails():
    # Read the text file containing the emails
    with open('emails.txt', 'r') as file:
        data = file.read()

    # Split the file content into an array of emails
    emails = data.strip().split('\n')

    # Headers and payload template for the POST request
    headers = {
        "accept": "application/json",
          "accept-language": "fr,fr-FR;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
          "canary": "PAQABDgEAAADnfolhJpSnRYB1SVj-Hgd8h7TAsheLRv7sR9z-9YRRACNkOAGAwkBMmYmPPeJ9-zxFLA7-4m2hXH9E5ZmIwFoodLLdVRY5btiq-hIxEtj1YLdfN046hRiJMP-aG2f5JBsuzXfl5DltBCCb_QoJuzUlO4YyAuaf5gkpr1V5ZcwsUJVU0zLD2Xr_SBhv-63tQCrHPR_LTGWIA_QRiXexc31B6gJOOMMjUWuMo-FqJk6trSAA",
          "client-request-id": "c3284b68-2977-f671-5487-9080b5470f9b",
          "content-type": "application/json; charset=UTF-8",
          "hpgact": "1800",
          "hpgid": "1104",
          "hpgrequestid": "61c44d37-3e17-472f-abd9-dd2fa3c64e00",
          "priority": "u=1, i",
          "sec-ch-ua": "\"Chromium\";v=\"124\", \"Microsoft Edge\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
          "sec-ch-ua-mobile": "?0",
          "sec-ch-ua-platform": "\"Windows\"",
          "sec-fetch-dest": "empty",
          "sec-fetch-mode": "cors",
          "sec-fetch-site": "same-origin",
          "x-edge-shopping-flag": "0",
          "cookie": "MicrosoftApplicationsTelemetryDeviceId=c07be452-07ce-431b-8832-404072412cfe; brcap=0; MSFPC=GUID=45a39aa0b4a14343856664d4652c68e3&HASH=45a3&LV=202403&V=4&LU=1711347790590; ESTSSSOTILES=1; AADSSOTILES=1; wlidperf=FR=L&ST=1714965105018; x-ms-gateway-slice=estsfd; stsservicecookie=estsfd; ESTSAUTHLIGHT=+0f9aa323-642c-4ebd-b7b8-ca062deba67b+f42e8a4d-51d2-4bbb-a2e9-400c53e17513+d5ccb849-1e5e-49b2-8986-38ab5d3db5d4; CCState=Q293QkNobHViM1JwWm1sallYUnBiMjVBWjNKaFpHbG1lUzV6YVhSbEVnRUJJZ2tKZ0twV0lwNDkzRWdxQ1FrM2VWc2FVM0RjU0RJcUNoSUtFQUlBQUFBQUFQRVB6Z0FBQUFBQUFBQVNDUWtOWEdBKzBtcmNTQm9KQ1RmNU9YSjNhTnhJT0FCSUFGSVNDaERwbjJmWEYvYnFRcFptdkZGeTMzQ0NXaElLRURSc1hIT2w3UlpDdlZVb3B3TEFKaTBLaHdFS0ZHTnZiblJoWTNSQVozSmhaR2xtZVM1emFYUmxFZ0VCSWdrSkFLOSt0dElpM0VncUNRbUlwa1AvVVhQY1NESXFDaElLRUFJQUFBQUFBUEVQemdBQUFBQUFBQUFTQ1FtYWFpd2owVzNjU0JvSkNZZ21JbGQyYTl4SU9BRklBRklTQ2hEcG4yZlhGL2JxUXBabXZGRnkzM0NDV2hJS0VNYnJBdzEyVlNWTm1ZQ3FGZEllRTdZS2NRb1VjbVZ3YkhsMGIwQm5jbUZrYVdaNUxuTnBkR1VTQVFBeUtnb1NDaEFDQUFBQUFBRHhEODRBQUFBQUFBQUFFZ2tKL3lLdjhnSnUzRWdhQ1FtMVJsSW1xR3ZjU0RnQ1NBQlNFZ29RNlo5bjF4ZjI2a0tXWnJ4UmN0OXdnbG9TQ2hDd3BzcVEyZmFhUnFlRXNHVkRJRlIzQ29jQkNoUmtiM1JqYjJSbFFHZHlZV1JwWm5rdWMybDBaUklCQVNJSkNZQ1kyekpjVnR4SUtna0pQQndIYy85MDNFZ3lLZ29TQ2hBQ0FBQUFBQUR4RDg0QUFBQUFBQUFBRWdrSnZIb2haYlp3M0VnYUNRbmJFd2FaVzI3Y1NEZ0RTQUJTRWdvUTZaOW4xeGYyNmtLV1pyeFJjdDl3Z2xvU0NoRFhFL0hyRmc5clM2N1dxYk13OHJ0R0VoSUtFQmJiUURqM1RsdEhwQnhQNkl2Z1k1WWFDUW12N0FXWlcyN2NTRExSQVFJQUFSOEJBQUFBNTM2SllTYVVwMFdBZFVsWS9oNEhmQUlBN1A4RkFQVC9TYnhTcWdmY043R1lyREEvMFg4SldwQVNGMTJWUjJ5Tk1iNnpqckx5R3ZSb0pXZHdVL1dyemRxa2xMd2JaTDNaayt4dnB1eXlORjJDc0E5dWtpV2RjdGwzQk5KRGVtUUNNdytsOG9FMXJTSXZ4Y2JjTFliekVDTGpTR2ZZTzRsT3FlUFFxKzlCaE1mN0VtbDBQdzQ1cDhSOUVFWkgrRk1DR1RnVzcwczFnaWxicWZTdWtXUm11Szh3R1poTS9sdEFaaUk0cmNtRGlvWEFGZGFnUURINzZQSUNhSWd5NFZiWXRzR3U0azg2ZGdScQ==; SignInStateCookie=CAgABFgIAAADnfolhJpSnRYB1SVj-Hgd8AgDs_wUA9P94CbPnXZc0MDXZZ8NqONmaB-svP75aI14-t8z3DCDbzS6HkZ8GcY_jXFwzazCRm5ZmAVeeo0YMKvOZHsYMQN-44jeBipXg1Qcsy8k0SiGLW5vOQ6QubC5pXvRKnLoyq3M_tt8M4kp34-GllJV3hoRiBA2hrrCggX-09c5J3wpIn_iMQo12lXjWQtSC1l5_o_bjsqpBhfnJaFt29Ji-RrgeARlkTZKJ4NJSPydKF_OItxcwmSn4JtrLuqj7Iw; esctx-LPzYKO13goQ=AQABCQEAAADnfolhJpSnRYB1SVj-Hgd8Qn9DEkN7fF41djHghBKZ79sQkzHFHW1K8SNc82vIW0VysDOCB0yHmE2t8KUhlT79CoJllFE2uXvDaUh8T5A9DyJq7QzGELlIsxL1fCwxBR43Y9MLgehJs1VLMsolLNIHtBD6p-e5EiXnPvLUWGnJ5iAA; esctx-sVCbnUZ8FAU=AQABCQEAAADnfolhJpSnRYB1SVj-Hgd8wnqV-wPxSvhQLJqCROOfH4V6hoxhz2OQIqpo96cfjgb-mHe-3HtNzlv4ppggSSDu2SjaTHSCdtq0nAK2Sayu7NXd7X_iP0vNJbWL3gx5IkMmsSd-Rc52PAh8DFKx6E-BUuNOg_4xnMpVqvBbN4K1cSAA; esctx-ma514y47MQ=AQABCQEAAADnfolhJpSnRYB1SVj-Hgd8-emdRCSzZVq8vGKAGJIRPePQuuVVkY8lRRB4bLTF-7KGC-zL5b3VI2zwwBGIT3UHRfUsD04P2eLDNGjw8cgTN4qqhw_StHcvornevdX7WsjuVarfiVqcfIByYeTT8H40dy31TS8IPrluDaV8_oZ9JCAA; esctx-yGJ2qdELwPU=AQABCQEAAADnfolhJpSnRYB1SVj-Hgd84AH4nq8c1-QCbKWv1nvEIdytj8nC-GgsTPlwZAwi37lAZhpu-u_cwUrZ-TTUC6GHeD95rA6AbVZs5dq_kjgbJ9qBqtKYCB7Ry8SMCYH-4KDJVyDVjNhNthnMZqft0grt3Ibu8rlwJGHUs_IE0SZh9SAA; esctx-Eg72WqOjUU=AQABCQEAAADnfolhJpSnRYB1SVj-Hgd82zIA7jK_RaC0SWscEWlrWsOXOTtyCsVmJCYTbAH6ypzQiSlV5sBticx1jy_vyZFke3CMUgLca9i7rgomjFhP1223PhZjrbTUeclxAKL5fIebNymBjSTLf3JzU-wfcqK1chGq9CtqshMF1onG9UE4eiAA; ESTSWCTXFLOWTOKEN=AQABIQEAAADnfolhJpSnRYB1SVj-Hgd8K2reC0xXMeDetLdEsAjgwnvAmU3NBx8VLDS1vdZabbjc8iqMDalQ6zzQrBFKHCFn3k2C0s9jfixWM4dPXVpsNU-YUSj1heGNCINZ9BTREILpoxUB_5UZ8gMZoOsqR88VjA8IQJRze52g9z80Vh4ArKqUMRmdJWgGx5-t_kNhKXAXlfRXvNBYlEEObkXjasf2LsdECnMgMgjsE89Y0CYy3-YjIzoMxnDYcR1YNatvGZ3PDI5qvRd2nijKLxv1PXw_5mpB_1qejCW6643M5pIkTnVqp2VJlbqQaSHBhtgxHfJgjdf8ay2Iv3AqbuGe-N2dFVEsPw9ynklq0NA_nNkt-VOiMme56HnyMUd_xnVYOaS8onv3tFrWIgKhSwC3RjcUd-fpzVw9QuA12kiGVi_J6qnKuKzlW04LpjGkQc-3W7f6jiVg1aalBDuW-jouOjoHXw_RYVN0YD4nTr5Ig6gczDGaOEF0GSSmCyrtH6v55cWCp0J8qry59OO5hQ8o6Nccd2VItni8fxPvtZk2C7qP6TfuLBqiBIp5PIVAgvgmt1hEptBN3utjXVyZz2afYuzX8AW7EvEZ5LukYj_GaXM2LSkROYHcfdLgFm0jsqF_kKA0jducbD2Li3F_0C2G4_lUDMbFgLjJ4ky2cO9OyBJ_M524c6SwntqEYSIjk8xFEiou8nwqGo6QYHqOrFRXLOUThh45BhIbaKQrfGZTa8-LQjIAx8WzgMHqJEyFy9_8QIKQX784jJLgBySMNqR2DJ1-Jv755et6DxH8yzZckbMYRA_TUpsNo3oaNOTb8YKPZnH0rI8nimk4NnZi43aSX7i6AFumnZ6f_CTlgRvidfaWNh584SRktLCHsTefq8EhZJXQUmdQ0CeWi3c-sPIi73_mG84FPkJYL7_NBg3U_uN0GHiZaDsnZXUHKNUc9nUMgp6n3sEoKNHXOauAreEqdFFmmQziOIniHicCPjTHS4GFLUL2Fu0hTY3h8vpgrz9owFcgLFUtXGAVInJfxoez80DbmVctil70qBVrdfCNKb5TMZniHtX-nzVpeBDc4AB0F1kLBI2vAguVC-9IsVhwrnnMqXSg6JWmaKcvi2JK66m9M7JL5oML4-EhQpchuTvZK7oPqvqvK5TS59roiUAcZfOqI6LNJOGb0AMMJhraCb1iAwQbvMnbW4str28rSe3de7d-yfHh4fz3gDJxutlXQyArWUx8cqHEp8rZBGvZoEDtBgvBIhiRFWMb0gfN-YoWCSSO4rfmikQ6IW1vyHxpuQqEZKaijgx-RgkSFgBRlbG6w7c_VEqTzbqijpOQ1g7wvmSYyH9DuCyiNwuOvhNIT2JPoSwtO7OPIlNloHeMi5eB7YSu0fx0IVIVm3DCRJ8qUGfPVEMELC4jX4ga9G4oDE54AGaBiJu6uwAb6bhIfbgqdjnNj2qjvFcD2FpUCqpTBYGyrrKeEzv_v5XdRYNhjlB2JjM4dXmYKdy1qqwScymPqx3d7D-LxI5jzF9LTulWtlCmGhxlLz9KA7afEhS5FG7CIeW-FGPhKKPohLatk_6Iy0fUMSSWJfmlBAt2t-GB_uCBR4ss6HXX4pkliQV7Z4MnT8fjFlBAFFHRW8zIQeLJdO1w5ogDSze4ETCQ95mgtOz4TIdQ0m8rdLnJX_-H8hw1Wjnrqp5iD_kmw8NWd2W3xlbYlnaVzBGnb7gtSMrg3-6KIu3Agqc8-uLU0070-uW_T_US7vVbT6k6ucufO-2oXHQfKbpbpb4ceCDNESjWuyAc4bryTw-NMwjUgtwwMjuSKouXmvpolrb5yrFzXEtymrhPQvTVmEZoG_UgOC0uhP3UoEpvbDWr-B3_fc36-N4wHFNDoAbtuV68PmijWVJXo-2eiW5G5PDqrpXemQOKmVP_PKMKgyHJbStAikrzNa-EAyyR3gs4ybB4FZEd2V_N8MOyt3yO_-zTpgFJXnbrnk5VsrhCZ9a2zhwXe-U0EqY823hsvT2_faCoJ26VV3WmdIBI1a12m1gP2Jr0-m81Lo2R9wyE_vuBXYshdYNQiOsCOzM-P7Y6RV-GllPahz7wxV0AwwUtdM4Rg3UZxeHSjoH-VYP0t3aI8yWMkrTJulvEFinCa5G0YxNPUlX6qTl7E4H38k6cyhDDSlCosVvYkCYgAA; ESTSAUTHPERSISTENT=0.AUgA6Z9n1xf26kKWZrxRct9wgmAPfm8BlFtPmOLPFb1f1eOAAEQ.AgABFwQAAADnfolhJpSnRYB1SVj-Hgd8AgDs_wUA9P_rM9v53rGNbZoIaQVMynf5Ygy5g2xyFfN8LrfEyzQghOW48hHjKx3fN3Iwdzy8framVJ29_H7jvnxSZl-nLG9hvbeXMXtqJihk72Z0ji4Ng-mhLNIZjgEu-aLK-aza71IgvHYevW3PTN4FKlbTwgv9dOV5TgwvhobTfIXMBG1QGCJamPHyP00z4PwPz8rdLz6K1EjwbPFM0D1_6TJVCp8c26tUzjlaR40RJpH3S_6Mb1yjPyubjSf8d9zPKFLUSR0HwQFa-6DBMBEdWTpbnCWM51nUto6--YLCl7VFR1QrmtSpE8GtgvrrlkLDlSP-d2FaF9e6X633TGI1slLPAqe0vGc4lSDkA3iAbHSHfiDuaxwMh0RHnlAuRrq_yOLKk_9KxvE_spz5mr2Cad5wwcZJigOdgDTYiY-WufcxOqh4sKrW8rtF6nQn66qndnH6DGfDH9EUM-8uGCHloCROXairwanV0xrKUX7idq3yDAq6zHTV4bkGtppazsd3uHYdm3KEHe64MG85PH0vioDANLL842uqscCgU2oyPkqmKg8FQyGU2G1P70eUwHHnpSd2T-BuDp-urmsjeDGjT0SF9zEmqOnXx4udOwZs8TfINErvnghbrJ8zM7VEMnM3xUZvEmwk9tXq4-j5GsHru_3Xo2oNs7LBuj5kYBu5fpDzXZ9Hm4Rxj4hPNApft-ESKM1K0iuxjtgKGUcWPisfu1ISZBixyp5g8I33G9YNOtVWDBymauyxt0TM1vWAdiN9wVWi5wwp5Fyq6OXRN5cO8UzxzvhNE7Ka2pKXWkWRZ8NYzuMXag0nPO6QeOsdkg7VgLz3ci-K17xDNsad0TMa8gY9Kx-nzyhdQyvTIBFPHAQo0E4TYiH3xhaj5fxEemkYIXynPsSvaw4dcXIOdTRCgH2O5grbMC4VUi9q-cutdWFujRcBXrMUFmu0gdGogbp2VXvgD5Nb3ekKHEIdoG3ZbELLVXHmCe7pfTpInxRYqts4p6jpXRSaom89f72CsW3hWffVin0YOYzqHcAd_exj8nFTqGtHK8zpVI2obqH-OKF0fBEMMpMG8yRD-y5SXC30r9xA6bHREFdfVdoDx_rKVGXYvUGNoVIsswoMrp9_KA32-EGCBh3ANrvCY4hABqeBn7VLdXoTBBmAod037roi56dgC7J0ffnsdBpdliiVcMHk24XQVclEbFrNWmJNQNClwWLjJ-mC7e1hz3kfwtTy-HASn6mGNQkrSoHB3Ft1yHHaCkU9R3oqhttuMwj95XJV4l3IA7DkeYzNYoX3DuFH73CXSdyz_hnyideo_Q3twwTwvPC2FSdGJ33OPnAp2TrdVY5rAr_IHfAxGnZ3kRkejALOb2U5qX-wklA34ip8y3Ib730PtAjyHED3Y588f5oGanxKfk5W80_gbqh-3DeB-oxektu9xPz4VllecCEyNFz_ZxQMFjiNjLrd6mcAU4x68ous7an5idZY-jt3yLP75XPAd0xkmUVU1Q-qTQ_tzepLOHSQ9LWFzAGxudvGNHg0Z-MKpZiHvbpIkb-3cdSyW_rD3UQIyk-_FFTeCU-IP232oZb9idET14UhpgpWDk9Qvgb3SMIhJwOXn70KLeIs09yc6zsaN45A2lqIsp2cqSirWayHG8ErOHiawnJ2BLV6pavaxuxfKWIyrwDYWuxKQQLp7U5uoKHqKwdr8RoTzytY-Ock5JJZrBs; ESTSAUTH=0.AUgA6Z9n1xf26kKWZrxRct9wgmAPfm8BlFtPmOLPFb1f1eOAAEQ.AgABFwQAAADnfolhJpSnRYB1SVj-Hgd8AgDs_wUA9P_gJyYjnafdTPQmJ2VbkrZ41zztNOwqHJOkKX6yrgBZozAE2mkBIdn2mIpe0mgDay7lkB4565C2_Q; buid=0.AUgA6Z9n1xf26kKWZrxRct9wgmAPfm8BlFtPmOLPFb1f1eOAAEQ.AQABGgEAAADnfolhJpSnRYB1SVj-Hgd83jaH5ILIQZmF_gSi99FziLPah-UYwRM8KpqZY3mgZtIFMzurd1RerHr72LHkg8UGx2npJmDbtZW3kYwwGXucrLGy_l9LB8JYXgHMiGXmtPpYEt1Qjh9cLWaZCOf2otq9V6MHRFvFEuN1PYVrAdc37tPaYparrZhjEnl5db2UIkkgAA; esctx=PAQABBwEAAADnfolhJpSnRYB1SVj-Hgd832rETJbiwy6qz8hXtRwuFTwUk9rn0JYTLDH6B1O1LBSXJ3ZQ4McPwi7f-zG9rugjgj2TslQgRrMv17wIZgvn7INtnr823e19Km8G296w5Hi9TJcwZFZD6FUja2vVypweU8cPrKfjdpUSncO0rgIZoDuYIYLzL7FpYjgZEoCjir8gAA; esctx-ZLFSjorU8o=AQABCQEAAADnfolhJpSnRYB1SVj-Hgd8Jy-Il7Dh6wHKyQ8WH--b6MfIULjSI4qYWJmgmpGZMs55uGVgZBDj-0nlFR_S7eApF09dZ11blExKvhBHEm_iLlwin4jjLESvjnl44OtiQDNfArVr79RRC1NPAp6kbpj65c7ag5aVVegWElI26fwFgCAA; fpc=AjVFpO3fDFRBn_rMQdIXfE-erOTJAQAAAF_Oy90OAAAA",
          "Referer": "https://login.microsoftonline.com/common/oauth2/authorize?client_id=00000002-0000-0ff1-ce00-000000000000&redirect_uri=https%3a%2f%2foutlook.office.com%2fowa%2f&resource=00000002-0000-0ff1-ce00-000000000000&response_mode=form_post&response_type=code+id_token&scope=openid&nonce=638506593795342746.dac04bcc-a381-43b9-9999-6147f7a244ae&msaredir=1&client-request-id=c3284b68-2977-f671-5487-9080b5470f9b&protectedtoken=true&claims=%7b%22id_token%22%3a%7b%22xms_cc%22%3a%7b%22values%22%3a%5b%22CP1%22%5d%7d%7d%7d&prompt=select_account&state=DYu9DoIwGEVB34UNKbS0dCAOJsZBjQENyEK-_phoREgpEN7enuSc6V7f87ytc-P0kYvHKM5SRFOOGU8xSRihOwUSESFlCDiLQ4IFD7kjpDFhLwYJIaB9952jfoFoP5i-G2w-6q-WtgUp--lnA5C2XGxuzaSD0YLVeRwYrd7Gje59DqcCydOFnlc-q7oYRcLNueNd030_TZl-RIJmUR0HccjaZ3VFD6zQrS5WVT3-&sso_nonce=AwABEgEAAAACAOz_BQD0_4WBMZ8R8Yfjl3W3N9qcgUbcIkiMfNIt1LOX-kLE7ZD5R4jn_mlEOzrf6MT0hB3q5g-trN8ZdGVrjz-ArfkNd1QgAA&mscrid=c3284b68-2977-f671-5487-9080b5470f9b",
          "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    payload_template = {
        "username" : "",
          "isOtherIdpSupported": True,
          "checkPhones": False,
          "isRemoteNGCSupported": True,
          "isCookieBannerShown": False,
          "isFidoSupported": True,
          "originalRequest": "rQQIARAAjZE7bNNgAIT916lpS6FRJyZAplPBie34EQd1cPNs04bY5FlAkfPHTl3H-RPHzqvq3rEzbEgsBSSEkECdQAxIFUidO1EGVHVAqFMlFhKxsME3nG46ne4WcSbARBboP7DUWCnaMBgK6mP3F878jH-3_4G9SzpzX265H7-JqLIPbmy6bqsTCQaR5zYQsgLIMEyoByCyg6inBd8BcATAKQD7E6IQCvO0ILC0GJbCLM_TTCBUoyWBZauUZrA0xfGCQYV5yFAsD3WJDWtsVYLHE3P3ZM_dZMeCHHOon09MG8ixKy3UcR_jb0AMemIMrcrxeExVjUqiaufLzWSxubJc1hQunrHtLSRZedMqRuVyti-6QzPkcZZSHpVHddVU04lBTpPzSjuxsdJPWJTUi6VpxcmVYT0mKEIbNhrxjpVQ7ZDSsbqmTosph7azYTZdzCc1MW1slRKZ_iBFu7mMHm23hValm20115mu1VZ5TluphUKSgNye6RiFHiW1c5V9_L9Wf40Toylt1DzECdTSm2btyAe--sCZb5bGI1NTM37sGnYTu_CBp5Ojg168PFl4eL4oP1soPZdL17HDySCTiZbLXJ0pQI-LrfW6PX2DH7SSCp1pdKvVdS0r3i94npeJpsJLQoTZI8AeQRwQ01O4HyPxaJY5JcBPAuxewg6m__X20WVwPMvNELChmXZnfnGbNGsVF1l6k4xsk327U4Fw7Lpaw9M7ZOQBOconH-3s7Ly_gl1c_X786dfbz09-pM7m7iznYauXpGVtkJX52G2kSvW4uYpKJio6HDvcGtbra1YhrXgQLb3yY78B0",
          "country": "SG",
          "forceotclogin": False,
          "isExternalFederationDisallowed": False,
          "isRemoteConnectSupported": False,
          "federationFlags": 0,
          "isSignup": False,
          "flowToken": "AQABIQEAAADnfolhJpSnRYB1SVj-Hgd8X1jhkOyj9Xy9ubwhoZWFpSFYQYKg4AneT1l1kt3Mw8tCmJpBMhOyeFsGh482yY7Z8BJlwgQL0uViyKLtoecB4Y-lA15V94rRLUcVW6lieD6s4X5vdm_0nOVUV3rULwBpDYPoIRRXq3RrG-m5yiHxB9791F1k38rTeOAO89li1D8hrS655QNJR55OoKdxgcCOC2t3HW1pBvMe5f3R7i4lhx0XT8X89lOBJ_MVyGZZnD_oeR0XymZT218lewWr6dBYA73at0-oDRE1VMdIn5j6ztB3CnI95RLIudEBRcFpQbI4TsodiX_XAZfxYrMPGIL2M2hHcgLFn8o4W7aFxH2YnNNF1d0QuZNBnWHJPhRUXJ_NohCNI4ZWyD2KBXzUIHqZ7gxytgB4jNHxRo2M98iCu82nj8oV28_1WMYgmJJQEAl6OQ6HpK4Tzl_zivawz2AXwzssKzHRJ05p7KTxXvO3oyAA",
          "isAccessPassSupported": True
    }

    # Use ThreadPoolExecutor to check emails in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(check_email, emails, [headers]*len(emails), [payload_template]*len(emails))

check_emails()