import 'package:email_validator/email_validator.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

/// The class for handle user's data.
class ParseAPI {
  String domaine = "https://api.area-revenge.ninja";
  final String applicationId = "";
  final String key = "";
  String userId, sessionToken, firstName, lastName, username;
  bool firstTimeService = true;

  /// The function for login a user.
  Future<bool> loginUser(String login, String password) async {
    var url = '$domaine/auth/login?username=$login&password=$password';
    if (EmailValidator.validate(login)) {
      url = '$domaine/auth/login?email=$login&password=$password';
    }
    try {
      var resp = await http.get(url);
      if (resp.statusCode != 200) {
        print("Error: ${resp.reasonPhrase}, Status Code: ${resp.statusCode}");
        return false;
      }
      var body = json.decode(resp.body);
      this.userId = body['objectId'];
      this.sessionToken = body['sessionToken'];
      this.firstName = body['first_name'];
      this.lastName = body['last_name'];
      this.username = body['username'];
      this.firstTimeService = false;
    } catch (err) {
      print("Error whentrying to log user ! $err");
      return false;
    }
    return true;
  }

  /// The function for register the user.
  Future<bool> registerUser(
      String email, String password, String username) async {
    var url = '$domaine/auth/register';
    try {
      var resp = await http.post(url,
          body: {"username": username, "password": password, "email": email});
      if (resp.statusCode != 201) {
        print("Error: ${resp.reasonPhrase}, Status Code: ${resp.statusCode}");
        return false;
      }
      var body = json.decode(resp.body);
      this.userId = body['objectId'];
      this.sessionToken = body['sessionToken'];
      this.username = username;
    } catch (err) {
      print("Error when trying to register user ! $err");
      return false;
    }
    return true;
  }

  /// The function reset user password.
  Future<bool> resetPassword(String email) async {
    try {
      var resp = await http.post('$domaine/user/email',
          headers: {
            "Content-Type": "application/json",
          },
          body: json.encode({"email": email}));
      if (resp.statusCode != 200 && resp.statusCode != 202) {
        return false;
      }
    } catch (err) {
      print("Error when trying to reset password... $err");
    }

    return true;
  }

  /// The function to get user's action reaction.
  Future<List<dynamic>> getUserAreas() async {
    try {
      var resp = await http.get('$domaine/area/',
          headers: {"Authorization": "Bearer $sessionToken"});

      if (resp.statusCode != 200) {
        return [];
      }

      return (json.decode(resp.body) as List);
    } catch (err) {
      print("Error when trying to get user area list... $err");
    }
    return [];
  }

  /// The function for update active area.
  Future<bool> updateActiveArea(bool isActif, String areaId) async {
    try {
      var resp = await http.put('$domaine/area/$areaId/',
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer $sessionToken"
          },
          body: json.encode({'is_actif': isActif}));
      if (resp.statusCode != 200) {
        return false;
      }
      return true;
    } catch (err) {
      print("Error when trying to get user area list... $err");
    }
    return false;
  }

  /// The function to get the user Service connected.
  Future<List<dynamic>> getServiceUserConnected() async {
    try {
      var resp = await http.get('$domaine/services?auth=true',
          headers: {"Authorization": "Bearer $sessionToken"});
      if (resp.statusCode != 200) {
        return [];
      }
      return (json.decode(resp.body)['results'] as List);
    } catch (err) {
      print("Error when trying to get user area list... $err");
    }
    return [];
  }

  /// The function to get a service
  Future<List<dynamic>> getServices() async {
    try {
      http.Response response = await http.get(
        'https://api.area-revenge.ninja/services',
        headers: {"Authorization": "Bearer ${this.sessionToken}"},
      );
      List<dynamic> data = json.decode(response.body)['results'];
      return data;
    } catch (e) {
      return List<dynamic>();
    }
  }

  /// The function for create action reaction.
  Future<bool> createArea(dynamic body) async {
    try {
      var resp = await http.post('$domaine/area/',
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer $sessionToken"
          },
          body: json.encode(body));
      if (resp.statusCode != 202) {
        print('Body resp ${resp.body}');
        return false;
      }
      return true;
    } catch (err) {
      print("Error when trying to get user area list... $err");
    }
    return false;
  }

  Future<bool> deleteArea(String areaId) async {
    try {
      var resp = await http.delete('$domaine/area/$areaId/',
          headers: {"Authorization": "Bearer $sessionToken"});

      if (resp.statusCode != 202) {
        print('Body resp ${resp.body}');
        return false;
      }
      return true;
    } catch (err) {
      print("Error when trying to get user area list... $err");
    }
    return false;
  }

  Future<bool> revokeToken(String service) async {
    try {
      var resp = await http.delete('$domaine/service/$service',
          headers: {"Authorization": "Bearer $sessionToken"});

      if (resp.statusCode != 200 || resp.statusCode != 202) {
        print('Body resp ${resp.body} Status: ${resp.statusCode}');
        return false;
      }
      return true;
    } catch (err) {
      print("Error when trying to get user area list... $err");
    }
    return false;
  }
}
