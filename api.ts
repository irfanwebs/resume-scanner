import { env } from '$env/dynamic/public';
import type { AnalysisResult } from '$lib/types';

const API_URL = env.PUBLIC_API_URL || 'http://localhost:8000';

export async function analyseResume(
  file: File,
  jobDescription: string,
  onChunk: (chunk: string) => void,
  onComplete: (result: AnalysisResult) => void,
  onError: (error: string) => void
): Promise<void> {
  const formData = new FormData();
  formData.append('resume', file);
  formData.append('job_description', jobDescription);

  try {
    const response = await fetch(`${API_URL}/api/analyse/stream`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Request failed' }));
      onError(errorData.detail || `Server error: ${response.status}`);
      return;
    }

    const reader = response.body?.getReader();
    if (!reader) {
      onError('Streaming not supported');
      return;
    }

    const decoder = new TextDecoder();
    let buffer = '';
    let fullContent = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;

        try {
          const data = JSON.parse(line.slice(6));

          if (data.type === 'chunk') {
            fullContent += data.content;
            onChunk(data.content);
          } else if (data.type === 'done') {
            // Parse the complete JSON
            const cleaned = fullContent
              .replace(/^```json?\n?/g, '')
              .replace(/\n?```$/g, '')
              .trim();
            const result: AnalysisResult = JSON.parse(cleaned);
            onComplete(result);
            return;
          } else if (data.type === 'error') {
            onError(data.content);
            return;
          }
        } catch {
          // Skip malformed SSE lines
        }
      }
    }

    // If stream ended without 'done' event, try parsing what we have
    if (fullContent) {
      try {
        const cleaned = fullContent
          .replace(/^```json?\n?/g, '')
          .replace(/\n?```$/g, '')
          .trim();
        const result: AnalysisResult = JSON.parse(cleaned);
        onComplete(result);
      } catch {
        onError('Failed to parse analysis results. Please try again.');
      }
    }
  } catch (err) {
    onError(err instanceof Error ? err.message : 'Network error. Is the server running?');
  }
}
