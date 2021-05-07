import 'package:area_mobile/account/account.dart';
import 'package:area_mobile/api/parse.dart';
import 'package:area_mobile/services/servicePage.dart';
import 'package:flutter/material.dart';
import 'package:custom_switch/custom_switch.dart';

/// The home page class for view action reaction.
class HomePage extends StatefulWidget {
  HomePage({Key key, this.userName}) : super(key: key);
  static const routeName = '/home';
  final String userName;

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  List<dynamic> _areas = [];
  List<dynamic> _services = [];
  bool _longPress = false;
  bool _showFloat = true;
  ParseAPI _api;
  final GlobalKey<ScaffoldState> _scaffoldKey = new GlobalKey<ScaffoldState>();

  final GlobalKey<RefreshIndicatorState> _refreshIndicatorKey =
      new GlobalKey<RefreshIndicatorState>();

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance
        .addPostFrameCallback((_) => _refreshIndicatorKey.currentState.show());
  }

  /// The function for resfresh user's data.
  Future<Null> _refresh() {
    return _api.getUserAreas().then((areas) {
      _api.getServiceUserConnected().then((connected) {
        List<dynamic> connectedService = [];
        (connected as List).forEach((element) {
          if (element["connected"] != null && (element["connected"] as bool)) {
            connectedService.add(element);
          }
        });
        setState(() {
          _areas = areas;
          _services = connectedService;
        });
      }).catchError((onError) {
        print("Error when trying to pull service... $onError");
      });
    }).catchError((onError) {
      print("Error when try to pull trades !");
    });
  }

  @override
  Widget build(BuildContext context) {
    _api = ModalRoute.of(context).settings.arguments as ParseAPI;
    return Scaffold(
      key: _scaffoldKey,
      appBar: AppBar(
        title: Text(_api.username),
        actions: [
          IconButton(
              icon: Icon(Icons.account_box),
              onPressed: () {
                Navigator.of(context)
                    .pushNamed(AccountPage.routeName, arguments: _api);
              })
        ],
      ),
      body: RefreshIndicator(
        key: _refreshIndicatorKey,
        onRefresh: _refresh,
        child: Container(
          child: _areas.length == 0
              ? SingleChildScrollView(
                  physics: AlwaysScrollableScrollPhysics(),
                  child: Container(
                      height: MediaQuery.of(context).size.height * 0.8,
                      child: Center(child: Text("You don't have any area..."))))
              : ListView.builder(
                  itemCount: _areas.length,
                  itemBuilder: (context, index) {
                    return Stack(
                      children: [
                        GestureDetector(
                          onLongPress: () {
                            setState(() {
                              _longPress = true;
                            });
                          },
                          onTap: () {
                            if (_longPress) {
                              setState(() {
                                _longPress = false;
                              });
                            } else {
                              print(_areas[index]);
                            }
                          },
                          child: Center(
                            child: Container(
                              margin: EdgeInsets.only(top: 15),
                              width: MediaQuery.of(context).size.width * 0.95,
                              height: MediaQuery.of(context).size.height * 0.15,
                              decoration: BoxDecoration(
                                borderRadius:
                                    BorderRadius.all(Radius.circular(20)),
                                color: Colors.grey[200],
                                boxShadow: [
                                  BoxShadow(
                                      color: Colors.grey[100], spreadRadius: 2),
                                ],
                              ),
                              child: Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
                                children: [
                                  Container(
                                    margin: EdgeInsets.only(left: 10),
                                    child: Row(
                                      children: [
                                        Container(
                                          margin: EdgeInsets.only(top: 8),
                                          child: Text(
                                              "${_areas[index]['trigger'].toString().split('-')[0]} -> ",
                                              style: TextStyle(
                                                  fontSize: 21,
                                                  fontWeight: FontWeight.w500,
                                                  fontStyle: FontStyle.italic)),
                                        ),
                                        Container(
                                            margin: EdgeInsets.only(top: 8),
                                            child: Text(
                                                "${_areas[index]['reactions'][0].toString().split('-')[0]}",
                                                style: TextStyle(
                                                    fontSize: 21,
                                                    fontWeight: FontWeight.w500,
                                                    fontStyle:
                                                        FontStyle.italic))),
                                      ],
                                    ),
                                  ),
                                  Container(
                                      alignment: Alignment.center,
                                      child: CustomSwitch(
                                        activeColor: Colors.green,
                                        value:
                                            _areas[index]['is_actif'] ?? false,
                                        onChanged: (value) async {
                                          bool ok = await _api.updateActiveArea(
                                              value, _areas[index]['objectId']);
                                          if (ok) {
                                            _areas[index]['is_actif'] = value;
                                            setState(() {});
                                          }
                                        },
                                      ))
                                ],
                              ),
                            ),
                          ),
                        ),
                        if (_longPress)
                          Container(
                              margin: EdgeInsets.only(top: 5, right: 5),
                              alignment: Alignment.topRight,
                              child: IconButton(
                                  icon: Icon(Icons.remove_circle_outline,
                                      color: Colors.red),
                                  onPressed: () async {
                                    bool ok = await _api
                                        .deleteArea(_areas[index]['objectId']);
                                    if (ok) {
                                      WidgetsBinding.instance
                                          .addPostFrameCallback((_) =>
                                              _refreshIndicatorKey.currentState
                                                  .show());
                                      setState(() {});
                                      return;
                                    }
                                    setState(() {
                                      _showFloat = false;
                                    });
                                    _scaffoldKey.currentState
                                        .showSnackBar(SnackBar(
                                            content: Text(
                                                "Error cannot delete area ! Retry later",
                                                style: TextStyle(
                                                    color: Colors.red)),
                                            duration: Duration(seconds: 2)))
                                        .closed
                                        .then((value) => {
                                              setState(() {
                                                _showFloat = true;
                                              })
                                            });
                                  }))
                      ],
                    );
                  },
                ),
        ),
      ),
      floatingActionButton: _showFloat
          ? FloatingActionButton(
              tooltip: "Press to create Area",
              child: Icon(Icons.add),
              onPressed: () {
                Navigator.pushNamed(context, ServicePage.routeName,
                    arguments: {"api": _api, "services": _services});
              },
            )
          : Container(),
    );
  }
}
