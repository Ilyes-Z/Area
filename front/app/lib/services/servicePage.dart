import 'package:area_mobile/api/parse.dart';
import 'package:area_mobile/services/createServicePage.dart';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:flutter/widgets.dart';
import 'package:autocomplete_textfield/autocomplete_textfield.dart';
import 'package:flutter_swiper/flutter_swiper.dart';
import 'package:flutter_page_indicator/flutter_page_indicator.dart';

/// The class for create an action reaction.
class ServicePage extends StatefulWidget {
  static const routeName = '/service';
  ServicePage({Key key}) : super(key: key);

  @override
  _ServicePageState createState() => _ServicePageState();
}

class _ServicePageState extends State<ServicePage> {
  GlobalKey<AutoCompleteTextFieldState<String>> _firstKey = new GlobalKey();
  GlobalKey<AutoCompleteTextFieldState<String>> _secondKey = new GlobalKey();
  List<dynamic> dialog = [
    {
      "title": "This Tuto is for creating an AREA",
      "picture": "assets/area_1.jpg"
    },
    {"title": "Choose service for an Action", "picture": "assets/area_2.jpg"},
    {"title": "Choose service for a Reaction", "picture": "assets/area_3.jpg"},
    {"title": "And make it !", "picture": "assets/area_4.jpg"}
  ];
  List<dynamic> suggestions = [];

  /// The function for get the list of action reaction.
  List<String> _getList(String type, TextEditingController controller) {
    if (suggestions.length == 0 || controller.text.isEmpty) {
      return [];
    }

    List<String> triggers = [];
    try {
      var service = suggestions
          .firstWhere((element) => element['name'] == controller.text);
      service[type].forEach((e) => triggers.add(e['name']));
    } catch (e) {
      return [];
    }

    return triggers;
  }

  /// The function for get a string
  String _getString(String type, TextEditingController controller, int index) {
    if (suggestions.length == 0 || controller.text.isEmpty) {
      return "";
    }

    try {
      var service = suggestions
          .firstWhere((element) => element['name'] == controller.text);
      return service[type][index]['id'];
    } catch (e) {
      return "";
    }
  }

  /// The function for get an id.
  String _getId(String type, TextEditingController controller, int index) {
    if (suggestions.length == 0 || controller.text.isEmpty) {
      return "";
    }

    try {
      var service = suggestions
          .firstWhere((element) => element['name'] == controller.text);
      return service['objectId'];
    } catch (e) {
      return "";
    }
  }

  List<dynamic> _getParams(
      String type, TextEditingController controller, int index) {
    if (suggestions.length == 0 || controller.text.isEmpty) {
      return [];
    }

    try {
      var service = suggestions
          .firstWhere((element) => element['name'] == controller.text);
      return service[type][index]['parameters'];
    } catch (e) {
      return [];
    }
  }

  Widget _textInputField(GlobalKey key, String label,
      TextEditingController controller, List<String> suggs, double width) {
    return Container(
      margin: EdgeInsets.only(top: 20),
      width: width,
      child: SimpleAutoCompleteTextField(
        key: key,
        textSubmitted: (text) => setState(() {
          if (text != "") {
            print({"Text: ${controller.text}"});
          }
        }),
        suggestions: suggs,
        clearOnSubmit: false,
        controller: controller,
        decoration: InputDecoration(
            border:
                OutlineInputBorder(borderRadius: BorderRadius.circular(20.0)),
            labelText: label),
      ),
    );
  }

  Widget _myDropdownTriggers(List<String> possibilty) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
            margin: EdgeInsets.only(top: 25, left: 5),
            child: Text("When this happens...",
                style: TextStyle(
                    decoration: TextDecoration.underline,
                    fontWeight: FontWeight.w500,
                    fontSize: 18))),
        Container(
          width: MediaQuery.of(context).size.width * 0.95,
          decoration: ShapeDecoration(
            shape: RoundedRectangleBorder(
              side: BorderSide(width: 1.0, color: Colors.grey),
              borderRadius: BorderRadius.all(Radius.circular(5.0)),
            ),
          ),
          child: DropdownButtonHideUnderline(
            child: Container(
              margin: EdgeInsets.only(left: 15),
              child: DropdownButton(
                  value: _triggerValue,
                  onChanged: (value) {
                    setState(() {
                      _triggerValue = value;
                    });
                  },
                  items: possibilty.map((e) {
                    return DropdownMenuItem(
                      child: Text(e),
                      value: possibilty.indexOf(e),
                    );
                  }).toList()),
            ),
          ),
        ),
      ],
    );
  }

  Widget _myDropdownReactions(List<String> possibilty) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
            margin: EdgeInsets.only(left: 5),
            child: Text("Then do this !",
                style: TextStyle(
                    decoration: TextDecoration.underline,
                    fontWeight: FontWeight.w500,
                    fontSize: 18))),
        Container(
          width: MediaQuery.of(context).size.width * 0.95,
          decoration: ShapeDecoration(
            shape: RoundedRectangleBorder(
              side: BorderSide(width: 1.0, color: Colors.grey),
              borderRadius: BorderRadius.all(Radius.circular(5.0)),
            ),
          ),
          child: DropdownButtonHideUnderline(
            child: Container(
              margin: EdgeInsets.only(left: 15),
              child: DropdownButton(
                  value: _reactionValue,
                  onChanged: (value) {
                    setState(() {
                      _reactionValue = value;
                    });
                  },
                  items: possibilty.map((e) {
                    return DropdownMenuItem(
                      child: Text(e),
                      value: possibilty.indexOf(e),
                    );
                  }).toList()),
            ),
          ),
        ),
      ],
    );
  }

  Widget _myDropDown() {
    var triggers = _getList("triggers", _firstApp);
    var reactions = _getList("reactions", _secondApp);
    if (_firstApp.text.isEmpty ||
        _secondApp.text.isEmpty ||
        triggers.length == 0 ||
        reactions.length == 0) {
      return Container();
    }
    return Column(children: [
      _myDropdownTriggers(triggers),
      Container(
          margin: EdgeInsets.only(top: 15),
          child:
              IconButton(icon: Icon(Icons.arrow_circle_down), onPressed: null)),
      _myDropdownReactions(reactions),
      Container(
          margin: EdgeInsets.only(top: 20),
          child: RaisedButton(
              child: Text("Make an AREA !"),
              onPressed: () {
                Navigator.of(context)
                    .pushNamed(CreateServicePage.routeName, arguments: {
                  "api": _api,
                  "action_id": _getId("triggers", _firstApp, _triggerValue),
                  "reaction_id": _getId("reactions", _secondApp, _reactionValue),
                  "action_type":
                      _getString("triggers", _firstApp, _triggerValue),
                  "reaction_type":
                      _getString("reactions", _secondApp, _reactionValue),
                  "action": _getParams("triggers", _firstApp, _triggerValue),
                  "reaction":
                      _getParams("reactions", _secondApp, _reactionValue)
                });
              }))
    ]);
  }

  _showMaterialDialog() {
    showDialog(
        context: context,
        builder: (_) => AlertDialog(
              title: Text("Create an AREA"),
              content: Container(
                height: MediaQuery.of(context).size.height * 0.5,
                child: Swiper(
                  indicatorLayout: PageIndicatorLayout.COLOR,
                  viewportFraction: 0.8,
                  scale: 0.7,
                  pagination: new SwiperPagination(),
                  itemCount: dialog.length,
                  itemBuilder: (BuildContext context, int index) {
                    return Column(
                      children: [
                        Text(dialog[index]['title']),
                        Container(
                          height: MediaQuery.of(context).size.height * 0.4,
                          child: Image.asset(
                            dialog[index]['picture'],
                            fit: BoxFit.fill,
                          ),
                        )
                      ],
                    );
                  },
                ),
              ),
              actions: <Widget>[
                FlatButton(
                  child: Text('Got it !'),
                  onPressed: () {
                    _api.firstTimeService = false;
                    Navigator.of(context).pop();
                  },
                )
              ],
            ));
  }

  TextEditingController _firstApp = TextEditingController();
  TextEditingController _secondApp = TextEditingController();
  int _triggerValue = 0;
  int _reactionValue = 0;
  ParseAPI _api;

  @override
  Widget build(BuildContext context) {
    var args = ModalRoute.of(context).settings.arguments as dynamic;
    _api = args['api'] as ParseAPI;
    suggestions = args['services'] as List;
    if (_api.firstTimeService) {
      SchedulerBinding.instance
          .addPostFrameCallback((_) => _showMaterialDialog());
    }
    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
            icon: Icon(Icons.arrow_back_ios),
            onPressed: () {
              Navigator.of(context).pop();
            }),
        title: Text("Create AREA"),
      ),
      body: SingleChildScrollView(
          child: Center(
        child: suggestions.length == 0
            ? Center(
                child: Container(
                    margin: EdgeInsets.only(
                        top: MediaQuery.of(context).size.height * 0.38),
                    child: Text("You are not connected to our service...")))
            : Column(
                children: [
                  Container(
                    width: MediaQuery.of(context).size.width * 0.98,
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        _textInputField(
                            _firstKey,
                            "Connect this app...",
                            _firstApp,
                            List<String>.from(
                                suggestions.map((e) => e['name'])),
                            MediaQuery.of(context).size.width * 0.42),
                        Container(
                          margin: EdgeInsets.only(top: 20),
                          child: IconButton(
                            onPressed: () {
                              setState(() {
                                var tmp = _firstApp.text;
                                _firstApp.text = _secondApp.text;
                                _secondApp.text = tmp;
                                _triggerValue = 0;
                                _reactionValue = 0;
                              });
                            },
                            icon: Icon(Icons.compare_arrows, size: 30),
                          ),
                        ),
                        _textInputField(
                            _secondKey,
                            "with this one !",
                            _secondApp,
                            List<String>.from(
                                suggestions.map((e) => e['name'])),
                            MediaQuery.of(context).size.width * 0.42),
                      ],
                    ),
                  ),
                  _myDropDown()
                ],
              ),
      )),
    );
  }
}
