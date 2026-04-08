import React, { useState } from "react";

function Register() {
  const [userName, setUserName] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = () => {
    // Registration logic here
  };

  return (
    <div>
      <h1>Sign Up</h1>
      <form>
        <input type="text" placeholder="Username" onChange={(e) => setUserName(e.target.value)} />
        <input type="text" placeholder="First Name" onChange={(e) => setFirstName(e.target.value)} />
        <input type="text" placeholder="Last Name" onChange={(e) => setLastName(e.target.value)} />
        <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
        <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
        <button onClick={handleRegister}>Register</button>
      </form>
    </div>
  );
}

export default Register;
