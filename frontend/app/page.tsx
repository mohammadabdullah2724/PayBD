import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="page-shell">
      <section className="hero-card">
        <span className="eyebrow">PayBD</span>
        <h1>Bangladesh payroll management, ready to launch.</h1>
        <p>
          The backend API is in place and the frontend now has a real authentication flow for sign-in
          and account creation.
        </p>
        <div className="button-row">
          <Link href="/login" className="button">
            Open login
          </Link>
          <a
            href="/api/v1/health"
            className="button secondary"
            target="_blank"
            rel="noreferrer"
          >
            API health
          </a>
        </div>
      </section>

      <section className="status-grid">
        <article className="status-card">
          <h2>Auth</h2>
          <p>Register new users and sign in against the FastAPI JWT endpoints.</p>
        </article>
        <article className="status-card">
          <h2>Employees</h2>
          <p>Next up: connect the employee routes to a dashboard and table view.</p>
        </article>
        <article className="status-card">
          <h2>Compliance</h2>
          <p>Built for Bangladesh payroll workflows with room for overtime and benefits modules.</p>
        </article>
      </section>
    </main>
  );
}
