import 'package:area_mobile/api/parse.dart';
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'dart:async';

/// The class for open and handle the webview.
class WebViewContainer extends StatefulWidget {
  final url;
  final title;
  final _api;
  WebViewContainer(this.url, this.title, this._api);
  @override
  createState() => _WebViewContainerState(this.url, this._api);
}

class _WebViewContainerState extends State<WebViewContainer> {
  ParseAPI _api;
  String _url;
  final _key = UniqueKey();
  Completer<WebViewController> _controller = Completer<WebViewController>();
  _WebViewContainerState(this._url, this._api);

  @override
  Widget build(BuildContext context) {
    _url = _url.replaceAll('<session_token>', _api.sessionToken);
    _url = _url.replaceAll('<hostname>', "${_api.domaine}/");
    print(_url);
    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.transparent,
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios),
          onPressed: () {
            Navigator.of(context).pop();
          },
        ),
      ),
      body: Column(
        children: [
          Expanded(
            child: WebView(
              key: _key,
              javascriptMode: JavascriptMode.unrestricted,
              initialUrl: _url,
              navigationDelegate: (nav) {
                if (nav.url.startsWith("https://api.area-revenge.ninja/")) {
                  Navigator.of(context).pop();
                }
                return NavigationDecision.navigate;
              },
              onWebViewCreated: (webViewController) {
                _controller.complete(webViewController);
                webViewController.clearCache();
                final cookieManager = CookieManager();
                cookieManager.clearCookies();
              },
            ),
          ),
        ],
      ),
    );
  }
}
