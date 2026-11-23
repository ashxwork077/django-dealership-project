import React, { useState } from "react";
import "./Register.css";

export default function Register() {
  const [form, setForm] = useState({
    username: "", firstName: "", lastName: "", email: "", password: ""
  });
  const [message, setMessage] = useState("");
  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((previous) => ({ ...previous, [name]: value }));
  };
  const handleSubmit = (event) => {
    event.preventDefault();
    setMessage("Registration form ready. Connect the registration API to create an account.");
  };
  return (
    <main className="register-page">
      <section className="register-card">
        <h1>Sign-up</h1>
        <p>Create your DriveWise dealership account.</p>
        <form onSubmit={handleSubmit}>
          <label htmlFor="username">Username</label>
          <input id="username" name="username" type="text" value={form.username} onChange={handleChange} autoComplete="username" required />
          <label htmlFor="firstName">First Name</label>
          <input id="firstName" name="firstName" type="text" value={form.firstName} onChange={handleChange} autoComplete="given-name" required />
          <label htmlFor="lastName">Last Name</label>
          <input id="lastName" name="lastName" type="text" value={form.lastName} onChange={handleChange} autoComplete="family-name" required />
          <label htmlFor="email">Email</label>
          <input id="email" name="email" type="email" value={form.email} onChange={handleChange} autoComplete="email" required />
          <label htmlFor="password">Password</label>
          <input id="password" name="password" type="password" value={form.password} onChange={handleChange} autoComplete="new-password" minLength={8} required />
          <button type="submit">Register</button>
        </form>
        {message && <p role="status">{message}</p>}
      </section>
    </main>
  );
}
