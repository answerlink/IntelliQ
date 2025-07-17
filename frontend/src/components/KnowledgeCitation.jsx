import React from 'react';

export default function KnowledgeCitation({ citations }) {
  if (!citations || citations.length === 0) return null;
  return (
    <div style={{ marginTop: 8, fontSize: 12, color: '#888' }}>
      <div>知识库引用：</div>
      <ul>
        {citations.map((c, i) => (
          <li key={i}>{c}</li>
        ))}
      </ul>
    </div>
  );
} 