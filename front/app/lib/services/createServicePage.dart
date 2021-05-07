import 'package:area_mobile/api/parse.dart';
import 'package:flutter/material.dart';

// The class for fill the information needed for the action reaction.
class CreateServicePage extends StatefulWidget {
  static const routeName = '/service/create';
  CreateServicePage({Key key}) : super(key: key);

  @override
  _CreateServicePageState createState() => _CreateServicePageState();
}

class _CreateServicePageState extends State<CreateServicePage> {
  List<dynamic> _fields = [];

  Widget _textInputField(String label, int index) {
    return Container(
      margin: EdgeInsets.only(top: 20),
      width: MediaQuery.of(context).size.width * 0.95,
      child: TextFormField(
        validator: (text) {
          if (text == null || text.isEmpty) {
            return '$label can\'t be empty !';
          }
          return null;
        },
        onChanged: (value) {
          _fields[index]['value'] = value;
        },
        controller: _fields[index]['controller'],
        decoration: InputDecoration(
            border:
                OutlineInputBorder(borderRadius: BorderRadius.circular(20.0)),
            labelText: label),
      ),
    );
  }

  Widget _arrayInputField(String label, int index) {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            Container(
              margin: EdgeInsets.only(top: 20),
              width: MediaQuery.of(context).size.width * 0.65,
              child: TextFormField(
                controller: _fields[index]['controller'],
                decoration: InputDecoration(
                    border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(20.0)),
                    labelText: label),
              ),
            ),
            Container(
              margin: EdgeInsets.only(top: 18),
              width: MediaQuery.of(context).size.width * 0.32,
              child: RaisedButton(
                onPressed: () {
                  if (_fields[index]['value'] == null) {
                    _fields[index]['value'] = [];
                  }
                  (_fields[index]['value'] as List)
                      .add(_fields[index]['controller'].text);
                  _fields[index]['controller'].clear();
                  setState(() {
                    _fields = _fields;
                  });
                },
                child: Text('Add'),
              ),
            )
          ],
        ),
        Container(
          height: MediaQuery.of(context).size.height * 0.20,
          child: ListView.builder(
              itemCount: ((_fields[index]['value'] ?? []) as List).length,
              itemBuilder: (BuildContext context, int i) {
                return Center(
                  child: Container(
                      width: MediaQuery.of(context).size.width * 0.98,
                      child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(_fields[index]['value'][i]),
                            IconButton(
                              icon: Icon(Icons.remove_circle_outline),
                              onPressed: () {
                                (_fields[index]['value'] as List).removeAt(i);
                                setState(() {});
                              },
                            )
                          ])),
                );
              }),
        )
      ],
    );
  }

  Widget _itemList(BuildContext context, dynamic param, int index) {
    if (param["type"] == "string") {
      return _textInputField(param["name"], index);
    }

    if (param["type"] == "array") {
      return _arrayInputField(param["name"], index);
    }

    return Container();
  }

  ParseAPI _api;

  @override
  Widget build(BuildContext context) {
    var args = ModalRoute.of(context).settings.arguments as dynamic;
    _api = args['api'] as ParseAPI;
    var actions = args['action'] as List;
    var reactions = args['reaction'] as List;
    var action_type = args['action_type'] as String;
    var reaction_type = args['reaction_type'] as String;
    var action_id = args['action_id'] as String;
    var reaction_id = args['reaction_id'] as String;

    if (_fields.length == 0) {
      for (int i = 0; i < actions.length; ++i) {
        _fields.add({
          "type": "action",
          "controller": TextEditingController(),
          "name": actions[i]["name"],
        });
      }

      for (int i = 0; i < reactions.length; ++i) {
        _fields.add({
          "type": "reaction",
          "controller": TextEditingController(),
          "name": reactions[i]["name"],
        });
      }
    }

    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
            icon: Icon(Icons.arrow_back_ios),
            onPressed: () {
              Navigator.of(context).pop();
            }),
        actions: [
          IconButton(
              icon: Icon(Icons.save_alt),
              onPressed: () async {
                Map<String, dynamic> body = {};
                body['services'] = {
                  "trigger": action_id,
                  "reaction": reaction_id
                };
                body['trigger'] = {"id": action_type};
                int i = 0;
                if (_fields[i]['type'] == 'action' &&
                    _fields[i]['value'] != null) {
                  body['trigger'][_fields[i]['name']] =
                      _fields[i]['value'].toString();
                  i++;
                }

                body['reaction'] = {"id": reaction_type};
                for (int j = 0; j < _fields.length; ++j) {
                  if (_fields[j]['type'] == 'reaction' &&
                      _fields[j]['value'] != null) {
                    body['reaction'][_fields[j]['name']] =
                        (_fields[j]['value'].toString());
                  }
                }

                var ok = await _api.createArea(body as dynamic);
                if (ok) {
                  Navigator.of(context).pop();
                }
              })
        ],
      ),
      body: SingleChildScrollView(
        child: Center(
          child: Container(
            width: MediaQuery.of(context).size.width,
            height: MediaQuery.of(context).size.height,
            child: ListView.builder(
                itemCount: actions.length + reactions.length,
                itemBuilder: (context, index) {
                  if (index < actions.length) {
                    return _itemList(context, actions[index], index);
                  }
                  if (!((reactions[index]["not_required"] ?? []) as List)
                          .contains(action_type)) {
                    return _itemList(context, reactions[index], index);
                  }

                  return Container();
                }),
          ),
        ),
      ),
    );
  }
}
