'use client';

import axios from 'axios';
import Link from 'next/link';
import { type FormEvent, useEffect, useState } from 'react';

import { clearAuthTokens, getStoredAccessToken, saveAuthTokens } from '../../../lib/auth';
import api from '../../../lib/api';
import type { AuthTokens, LoginPayload, RegisterPayload } from '../../../types';

type AuthMode = 'login' | 'register';

function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail;
    return typeof detail === 'string' ? detail : 'Request failed. Please try again.';
  }

  return error instanceof Error ? error.message : 'Unexpected error. Please try again.';
}

export default function AuthPage() {
  const [mode, setMode] = useState<AuthMode>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [hasStoredSession, setHasStoredSession] = useState(false);

  useEffect(() => {
    setHasStoredSession(Boolean(getStoredAccessToken()));
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setMessage(null);

    if (mode === 'register' && password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setIsSubmitting(true);

    try {
      if (mode === 'register') {
        const payload: RegisterPayload = { email, password };
        await api.post('/auth/register', payload);
        setMessage('Account created successfully. Please sign in.');
        setMode('login');
        setPassword('');
        setConfirmPassword('');
      } else {
        const payload: LoginPayload = { email, password };
        const response = await api.post<AuthTokens>('/auth/login', payload);
        saveAuthTokens(response.data);
        setHasStoredSession(true);
        setMessage('Signed in successfully. Tokens were saved in local storage.');
      }
    } catch (submitError) {
      setError(getErrorMessage(submitError));
    } finally {
      setIsSubmitting(false);
    }
  }

  function handleClearSession() {
    clearAuthTokens();
    setHasStoredSession(false);
    setMessage('Stored session cleared.');
    setError(null);
  }

  return (
    <main className="page-shell auth-layout">
      <section className="hero-card compact">
        <span className="eyebrow">PayBD access</span>
        <h1>{mode === 'login' ? 'Sign in to your workspace' : 'Create your PayBD account'}</h1>
        <p>
          Use the FastAPI authentication endpoints to register, log in, and keep a saved session in
          your browser.
        </p>
        <p>
          <Link href="/" className="text-link">
            Back to home
          </Link>
        </p>
      </section>

      <section className="auth-card">
        <div className="tabs" role="tablist" aria-label="Authentication mode">
          <button
            type="button"
            className={`tab ${mode === 'login' ? 'active' : ''}`}
            onClick={() => setMode('login')}
          >
            Login
          </button>
          <button
            type="button"
            className={`tab ${mode === 'register' ? 'active' : ''}`}
            onClick={() => setMode('register')}
          >
            Register
          </button>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          <label className="field">
            <span>Email</span>
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="you@company.com"
              required
            />
          </label>

          <label className="field">
            <span>Password</span>
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Minimum 8 characters"
              required
              minLength={8}
            />
          </label>

          {mode === 'register' ? (
            <label className="field">
              <span>Confirm password</span>
              <input
                type="password"
                value={confirmPassword}
                onChange={(event) => setConfirmPassword(event.target.value)}
                placeholder="Repeat password"
                required
                minLength={8}
              />
            </label>
          ) : null}

          {message ? <p className="notice success">{message}</p> : null}
          {error ? <p className="notice error">{error}</p> : null}

          <div className="button-row">
            <button type="submit" className="button" disabled={isSubmitting}>
              {isSubmitting ? 'Working…' : mode === 'login' ? 'Sign in' : 'Create account'}
            </button>
            <button type="button" className="button secondary" onClick={handleClearSession}>
              Clear session
            </button>
          </div>
        </form>

        <div className="session-status">
          <strong>Status:</strong> {hasStoredSession ? 'saved session detected' : 'no saved session'}
        </div>
      </section>
    </main>
  );
}
