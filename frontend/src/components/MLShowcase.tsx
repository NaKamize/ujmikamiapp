import { useState } from 'react';
import './MLShowcase.css';

/* ── Types ────────────────────────────────── */
interface Link {
  label: string;
  url: string;
}

interface MLModelData {
  id: number;
  title: string;
  description: string;
  category: string;
  category_display: string;
  architecture: string;
  framework: string;
  competition_name: string;
  competition_url: string;
  dataset_description: string;
  metrics: Record<string, number | string>;
  rank: string;
  score: string;
  image: string | null;
  links: Link[];
}

/* ── Helpers ──────────────────────────────── */
function formatMetricKey(key: string): string {
  return key
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

function formatMetricValue(value: number | string): string {
  if (typeof value === 'number') {
    return value < 1 ? value.toFixed(5) : value.toFixed(2);
  }
  return String(value);
}

/* ── Single Model Card ─────────────────────── */
function MLModelCard({ model }: { model: MLModelData }) {
  const [detailsOpen, setDetailsOpen] = useState(false);

  return (
    <div className="ml-card">
      <div className="ml-card-header">
        <div className="ml-card-badges">
          {model.architecture && (
            <span className="ml-badge ml-badge-architecture">
              {model.architecture}
            </span>
          )}
          {model.category_display && (
            <span className="ml-badge ml-badge-category">
              {model.category_display}
            </span>
          )}
          {model.rank && (
            <span className="ml-badge ml-badge-rank">Rank: {model.rank}</span>
          )}
          {model.score && (
            <span className="ml-badge ml-badge-score">Score: {model.score}</span>
          )}
        </div>
        <h3 className="ml-card-title">{model.title}</h3>
      </div>

      <div className="ml-card-body">
        <p className="ml-card-desc">{model.description}</p>

        {/* Metrics grid */}
        {Object.keys(model.metrics).length > 0 && (
          <div className="ml-metrics">
            {Object.entries(model.metrics).map(([key, value]) => (
              <div key={key} className="ml-metric">
                <span className="ml-metric-key">{formatMetricKey(key)}</span>
                <span className="ml-metric-value">
                  {formatMetricValue(value)}
                </span>
              </div>
            ))}
          </div>
        )}

        {/* Links */}
        {model.links && model.links.length > 0 && (
          <div className="ml-card-links">
            {model.links.map((link, i) => (
              <a
                key={i}
                href={link.url}
                className="ml-card-link"
                target="_blank"
                rel="noopener noreferrer"
              >
                {link.label}
              </a>
            ))}
          </div>
        )}

        {/* Expandable details */}
        {(model.dataset_description || model.framework) && (
          <button
            className={`ml-details-toggle${detailsOpen ? ' open' : ''}`}
            onClick={() => setDetailsOpen(!detailsOpen)}
            aria-expanded={detailsOpen}
          >
            {detailsOpen ? 'Less' : 'More'} details
          </button>
        )}
      </div>

      <div className={`ml-details${detailsOpen ? ' open' : ''}`}>
        <div className="ml-details-inner">
          {model.dataset_description && (
            <>
              <h4>Dataset</h4>
              <p>{model.dataset_description}</p>
            </>
          )}
          {model.framework && (
            <>
              <h4>Framework</h4>
              <p>{model.framework}</p>
            </>
          )}
          {model.competition_name && (
            <>
              <h4>Competition</h4>
              <p>
                {model.competition_url ? (
                  <a
                    href={model.competition_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{ color: 'var(--accent)' }}
                  >
                    {model.competition_name}
                  </a>
                ) : (
                  model.competition_name
                )}
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

/* ── Showcase Section ──────────────────────── */
interface MLShowcaseProps {
  models: MLModelData[];
  loading: boolean;
  error: string | null;
}

export default function MLShowcase({ models, loading, error }: MLShowcaseProps) {
  const showEmpty = !loading && !error && models.length === 0;
  const showList = !loading && !error && models.length > 0;

  return (
    <section id="ml-showcase" className="section-gray">
      <div className="container">
        <span className="section-eyebrow">04 · ML Showcase</span>
        <h2>Machine Learning Projects</h2>
        <p className="section-lead">
          Kaggle competition entries and ML experiments — from NLP and computer
          vision to ensemble methods and transfer learning.
        </p>

        {loading && (
          <div className="ml-loading">
            <span>Loading models…</span>
          </div>
        )}

        {error && (
          <div className="ml-error">
            <span>⚠ {error}</span>
          </div>
        )}

        {showEmpty && (
          <div className="ml-empty">
            <span>No ML models to show yet. Check back later!</span>
          </div>
        )}

        {showList && (
          <div className="ml-models-list">
            {models.map((m) => (
              <MLModelCard key={m.id} model={m} />
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
