#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from caesar import encrypt
import cgi

import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)

EMAIL_RE = re.compile(r"^.{3,20}$")
def valid_email(email):
    return PASS_RE.match(email)

page_header ="""
<!DOCTYPE html>
<html>
    <head>
        <style>
            form {
                background-color: #eee;
                padding: 20px;
                margin: 0 auto;
                width: auto;
                font: 16px sans-serif;
                border-radius: 10px;
            }
            textarea {
                margin: 10px 0;
                width: 540px;
                height: 120px;
            }
            p.error {
                color: red;
            }
            span {
                color: red;
            }
            h2 {
                font-size:1.2em;
                text-align:center;
            }
            h1 {
                text-align:center;
            }
        </style>
    </head>

"""

page_footer="""
        </body>
    </html>
"""

body2="""
<h1>Signup</h1>
<form method="post">
    <table>
        <tr>
            <td><label for="username">Username</label></td>
            <td>
                <input name="username" type="text" value="" required>
                <p class="error"></p>
            </td>
        </tr>
    <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" required>
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" required>
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="">
                        <span class="error"></span>
                    </td>
                </tr>
    </table>
    <input type="submit">
</form>
</body>
"""

class Index(webapp2.RequestHandler):
    def get(self):
        body="""
        <body>
            <h1>Caesar Crypt</h1>
         <form method="post">
            <div>
                <label for="rot">Rotate by:</label>
                <input type="text" name="rot" value="0">
                <p class="error"></p>
            </div>
            <textarea type="text" name="text"></textarea>
            <br>
            <input type="submit"/>
        </form>
        """
        response = page_header + body + page_footer
        self.response.write(response)

    def post(self):
        body="""
        <body>
            <h1>Caesar Crypt</h1>
         <form method="post">
            <div>
                <label for="rot">Rotate by:</label>
                <input type="text" name="rot" value="%(userRot)s">
                <p class="error"></p>
            </div>
            <textarea type="text" name="text">%(userText)s</textarea>
            <br>
            <input type="submit"/>
        </form>
        """
        plainText = self.request.get("text")
        rot = int(self.request.get("rot"))
        text = cgi.escape(encrypt(plainText, rot), quote = True)
        self.response.write(page_header + body % {"userRot": self.request.get("rot"),
                                    "userText": text} + page_footer)

class UserSignup(webapp2.RequestHandler):
    def get(self):

        self.response.write(page_header + body2 + page_footer)

    def post(self):
        body2="""
        <h1>Signup</h1>
        <form method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="%(username)s" required>
                        <span class="error">%(error)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" required>
                        <span class="error">%(error_password)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" required>
                        <span class="error">%(error_verify)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="%(email)s">
                        <span class="error">%(error_email)s</span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>
        </body>
        """

        error = "That is not a valid username. Please try again"
        username = self.request.get("username")
        password = self.request.get("password")
        email = self.request.get("email")
        verify_password = self.request.get("verify")
        error_password = "That is not a valid password. Please try again"
        error_verify = "Your passwords do not match. Please try again"
        error_email = "That is not a valid email. Please try again"
        if not valid_username(username):
            self.response.write(page_header + body2 % {"error":error,
                                                       "username":username} + page_footer)
        if not valid_password(password):
            self.response.write(page_header + body2 % {"error":error,
                                                       "username":username,
                                                       "error_password":error_password} + page_footer)
        elif password != verify_password:
            self.response.write(page_header + body2 % {"error":error,
                                                       "username":username,
                                                       "error_verify":error_verify} + page_footer)
        if not valid_email(email):
            if not valid_password(password):
                self.response.write(page_header + body2 % {"error":error,
                                                           "username":username,
                                                           "error_email":email,
                                                           "email":email} + page_footer)
        else:
            self.redirect('/welcome?username=' + username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username2 = self.request.get("username")
        self.response.write(page_header + "<h1>Welcome, " + username2 + "</h2")

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/signup', UserSignup),
    ('/welcome', Welcome)
], debug=True)
