import React, { useEffect, useMemo, useState } from 'react';
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
  CircleMarker,
  Tooltip,
  useMap,
} from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// The layer toggle is the site's core scholarly contribution, so it is
// defined here (not buried in Leaflet's own corner control) and rendered
// as a prominent control bar above the map. A layer is one entry in this
// object plus a "layers" tag on the relevant places in sites.json.
//
// Two kinds of place share the map: sites visited in 2026 (solid markers,
// with a Field Journal entry) and places known only from the texts (hollow
// markers: the home towns of the iamata petitioners, the settings of the
// Epidemics). `route` is not a tag: it draws the trip itself, through every
// visited site in date order, plus any geotagged photos (photos.json).
export const LAYER_META = {
  'cult-healing': {
    label: 'Asklepieia visited',
    description: 'Healing sanctuaries of Asklepios visited in July–August 2026.',
    color: '#a3572c',
  },
  iamata: {
    label: 'Iamata: where petitioners came from',
    description:
      'Home towns named in the 43 tales of the two best-preserved Epidauros stelai (IG IV²,1 121–122), each joined to Epidauros.',
    color: '#6b4c7a',
  },
  hippocratic: {
    label: 'Hippocratic places',
    description:
      'Kos, and the towns where the Epidemics I and III constitutions and case histories are set: the physician travels to the patients.',
    color: '#3d6b73',
  },
  route: {
    label: 'My route, 2026',
    description: 'The fieldwork itinerary from Messene to Athens, 24 July – 2 August 2026.',
    color: '#4a4a4a',
  },
};

const WHOLE_MAP = { center: [38.6, 24.6], zoom: 6 };

function markerIcon(colors, { visited, region }) {
  const size = visited ? 20 : 16;
  const fill =
    colors.length > 1
      ? `conic-gradient(${colors.map((c, i) => `${c} ${(i * 360) / colors.length}deg ${((i + 1) * 360) / colors.length}deg`).join(', ')})`
      : colors[0] || '#888';
  // Visited: solid disc. Text-only: hollow ring (dashed for a region or
  // island, where the point is only approximate).
  const style = visited
    ? `background:${fill};border:2px solid #fdfbf5;box-shadow:0 1px 3px rgba(0,0,0,.35)`
    : `background:#fdfbf5;border:3px ${region ? 'dashed' : 'solid'} ${colors[0] || '#888'};box-shadow:0 1px 2px rgba(0,0,0,.3)`;
  return L.divIcon({
    className: 'site-marker',
    html: `<span style="display:block;box-sizing:border-box;width:${size}px;height:${size}px;border-radius:50%;${style}"></span>`,
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
    popupAnchor: [0, -size / 2 - 2],
  });
}

const photoIcon = L.divIcon({
  className: 'site-marker',
  html: '<span style="display:block;width:10px;height:10px;background:#4a4a4a;border:2px solid #fdfbf5;box-shadow:0 1px 2px rgba(0,0,0,.35)"></span>',
  iconSize: [10, 10],
  iconAnchor: [5, 5],
});

function FocusControl({ focus, epidauros }) {
  const map = useMap();
  useEffect(() => {
    if (focus === 'sanctuary' && epidauros) map.flyTo([37.5976, 23.0758], 16, { duration: 0.8 });
    else map.flyTo(WHOLE_MAP.center, WHOLE_MAP.zoom, { duration: 0.8 });
  }, [focus]);
  return null;
}

const formatDay = (iso) =>
  new Date(`${iso}T00:00:00Z`).toLocaleDateString('en-US', { month: 'short', day: 'numeric', timeZone: 'UTC' });

export default function SiteMap({
  sites,
  iamata = [],
  cases = [],
  photos = [],
  layers = ['cult-healing', 'iamata', 'hippocratic', 'route'],
}) {
  const [active, setActive] = useState(() =>
    Object.fromEntries(Object.keys(LAYER_META).map((k) => [k, layers.includes(k)]))
  );
  // Iamata filter: all tales, or only those whose story reaches beyond
  // Epidauros (the `away` note in iamata.json).
  const [taleFilter, setTaleFilter] = useState('all');
  const [focus, setFocus] = useState('all');

  const epidauros = sites.find((s) => s.id === 'epidauros');
  const placed = sites.filter((s) => s.lat != null && s.lng != null);
  const visibleTales = iamata.filter((t) => taleFilter === 'all' || t.away);
  const talesFrom = (id) => visibleTales.filter((t) => t.origin === id);
  const casesIn = (site) => cases.filter((c) => c.city && c.city === site.name);

  const shown = useMemo(
    () =>
      placed.filter((s) => {
        if (s.visited && active.route) return true;
        return (s.layers || []).some((l) => {
          if (!active[l]) return false;
          // A town that is only on the iamata layer drops out when the
          // filter leaves it with no tales.
          if (l === 'iamata' && !s.visited && s.id !== 'epidauros') return talesFrom(s.id).length > 0;
          return true;
        });
      }),
    [placed, active, taleFilter]
  );

  const pilgrimLines = active.iamata && epidauros
    ? placed
        .filter((s) => s.id !== 'epidauros' && (s.layers || []).includes('iamata') && talesFrom(s.id).length > 0)
        .map((s) => ({ site: s, count: talesFrom(s.id).length }))
    : [];

  const route = placed.filter((s) => s.visited).sort((a, b) => a.date.localeCompare(b.date));
  const unplaced = sites.filter((s) => s.lat == null && (s.layers || []).some((l) => active[l]));

  const activeDescriptions = Object.entries(LAYER_META)
    .filter(([key]) => active[key])
    .map(([, meta]) => meta.description);

  function toggleLayer(key) {
    setActive((prev) => ({ ...prev, [key]: !prev[key] }));
  }

  return (
    <div className="site-map">
      <div className="layer-toggle-bar" role="group" aria-label="Map layers">
        {Object.entries(LAYER_META).map(([key, meta]) => (
          <button
            key={key}
            type="button"
            className={`layer-toggle${active[key] ? ' is-active' : ''}`}
            aria-pressed={active[key]}
            onClick={() => toggleLayer(key)}
            style={{ '--layer-color': meta.color }}
          >
            <span className="layer-toggle__swatch" aria-hidden="true"></span>
            <span className="layer-toggle__label">{meta.label}</span>
          </button>
        ))}
      </div>

      <p className="layer-toggle-help">
        {activeDescriptions.length > 0
          ? activeDescriptions.join(' ')
          : 'No layers active — select a layer above to show sites.'}
      </p>

      <div className="map-options">
        {active.iamata && iamata.length > 0 && (
          <label>
            Tales:{' '}
            <select value={taleFilter} onChange={(e) => setTaleFilter(e.target.value)}>
              <option value="all">All {iamata.length}</option>
              <option value="away">Only stories that reach beyond Epidauros ({iamata.filter((t) => t.away).length})</option>
            </select>
          </label>
        )}
        {epidauros && (
          <span className="map-options__focus" role="group" aria-label="Zoom">
            <button type="button" aria-pressed={focus === 'all'} onClick={() => setFocus('all')}>Whole map</button>
            <button type="button" aria-pressed={focus === 'sanctuary'} onClick={() => setFocus('sanctuary')}>Epidauros sanctuary</button>
          </span>
        )}
      </div>

      <div className="site-map__frame">
        <MapContainer center={WHOLE_MAP.center} zoom={WHOLE_MAP.zoom} scrollWheelZoom={true} style={{ height: '100%', width: '100%' }}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors · places: <a href="https://pleiades.stoa.org">Pleiades</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <FocusControl focus={focus} epidauros={epidauros} />

          {pilgrimLines.map(({ site, count }) => (
            <Polyline
              key={`line-${site.id}`}
              positions={[[site.lat, site.lng], [epidauros.lat, epidauros.lng]]}
              pathOptions={{
                color: LAYER_META.iamata.color,
                weight: 1 + count,
                opacity: 0.55,
                dashArray: site.region ? '4 6' : null,
              }}
            />
          ))}

          {active.route && route.length > 1 && (
            <Polyline
              positions={route.map((s) => [s.lat, s.lng])}
              pathOptions={{ color: LAYER_META.route.color, weight: 2, opacity: 0.8, dashArray: '2 6' }}
            />
          )}

          {active.route &&
            photos.map((p) => (
              <Marker key={p.src} position={[p.lat, p.lng]} icon={photoIcon}>
                <Popup>
                  <div className="site-popup">
                    <img src={p.src} alt={p.caption || ''} className="site-popup__photo" />
                    {p.caption && <p>{p.caption}</p>}
                    <p className="site-popup__meta">{p.taken}</p>
                  </div>
                </Popup>
              </Marker>
            ))}

          {focus === 'sanctuary' &&
            (epidauros?.features || []).map((f) => (
              <CircleMarker
                key={f.name}
                center={[f.lat, f.lng]}
                radius={5}
                pathOptions={{ color: LAYER_META['cult-healing'].color, fillOpacity: 0.6 }}
              >
                <Tooltip permanent direction="right">{f.name}</Tooltip>
              </CircleMarker>
            ))}

          {shown.map((site) => {
            const colors = (site.layers || []).filter((l) => active[l]).map((l) => LAYER_META[l].color);
            const tales = talesFrom(site.id);
            const siteCases = casesIn(site);
            return (
              <Marker
                key={site.id}
                position={[site.lat, site.lng]}
                icon={markerIcon(colors.length ? colors : [LAYER_META.route.color], site)}
              >
                <Popup>
                  <div className="site-popup">
                    <h3>{site.name}</h3>
                    <p className="site-popup__meta">
                      {site.visited ? `Visited ${formatDay(site.date)} 2026` : 'Known from the texts; not visited'}
                    </p>
                    {site.shortDescription && <p>{site.shortDescription}</p>}
                    {site.note && <p className="site-popup__note">{site.note}</p>}

                    {site.id === 'epidauros' && iamata.length > 0 && (
                      <p>
                        Where the iamata stelai stood. <a href="/epigraphy#iamata">The catalogue of {iamata.length} tales &rarr;</a>
                      </p>
                    )}
                    {active.iamata && tales.length > 0 && (
                      <>
                        <p className="site-popup__label">Petitioners from here in the iamata</p>
                        <ul className="site-popup__list">
                          {tales.map((t) => (
                            <li key={t.n}>
                              <a href={`/epigraphy/iamata/${t.n}`}>{t.n}. {t.petitioner}</a>: {t.complaint}
                            </li>
                          ))}
                        </ul>
                      </>
                    )}

                    {active.hippocratic && (site.relatedHippocraticPassages || []).length > 0 && (
                      <>
                        <p className="site-popup__label">Constitutions set here</p>
                        <ul className="site-popup__list">
                          {site.relatedHippocraticPassages.map((slug) => (
                            <li key={slug}>
                              <a href={`/sources/hippocratic-corpus/epidemics/${slug}`}>
                                {slug.replace('constitution-', 'Constitution ')}
                              </a>
                            </li>
                          ))}
                        </ul>
                      </>
                    )}
                    {active.hippocratic && siteCases.length > 0 && (
                      <>
                        <p className="site-popup__label">Case histories set “In {site.name}”</p>
                        <ul className="site-popup__list">
                          {siteCases.map((c) => (
                            <li key={c.ref}>
                              {c.ref}{c.landmark ? `: “${c.landmark}”` : ''}
                            </li>
                          ))}
                        </ul>
                      </>
                    )}

                    {site.journal && <a href={site.journal}>Read the journal entry &rarr;</a>}
                    {site.pleiades && (
                      <p className="site-popup__meta">
                        <a href={`https://pleiades.stoa.org/places/${site.pleiades}`} target="_blank" rel="noopener">
                          Pleiades {site.pleiades}
                        </a>
                      </p>
                    )}
                  </div>
                </Popup>
              </Marker>
            );
          })}
        </MapContainer>
      </div>

      <ul className="map-legend-list">
        {Object.entries(LAYER_META).map(([key, meta]) => (
          <li key={key}>
            <span className="legend-swatch" style={{ background: meta.color }}></span>
            {meta.label}
          </li>
        ))}
        <li><span className="legend-swatch legend-swatch--solid"></span>Visited</li>
        <li><span className="legend-swatch legend-swatch--hollow"></span>Known from the texts only</li>
        <li><span className="legend-swatch legend-swatch--dashed"></span>Region or island (approximate)</li>
      </ul>
      {unplaced.length > 0 && (
        <p className="map-unplaced">
          Not on the map: {unplaced.map((s, i) => (
            <span key={s.id}>{i > 0 && '; '}<strong>{s.name}</strong> ({s.unplaced})</span>
          ))}
        </p>
      )}
    </div>
  );
}
