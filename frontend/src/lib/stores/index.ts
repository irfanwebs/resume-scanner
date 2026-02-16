import { writable, derived } from 'svelte/store';
import type { AnalysisResult, AnalysisState } from '$lib/types';

export const file = writable<File | null>(null);
export const fileName = writable('');
export const jobDescription = writable('');
export const analysisState = writable<AnalysisState>('idle');
export const analysisResult = writable<AnalysisResult | null>(null);
export const errorMessage = writable('');
export const streamedContent = writable('');

export const canSubmit = derived(
  [file, jobDescription, analysisState],
  ([$file, $jd, $state]) => {
    return $file !== null && $jd.trim().length > 20 && ($state === 'idle' || $state === 'complete' || $state === 'error');
  }
);

export function resetAnalysis() {
  analysisState.set('idle');
  analysisResult.set(null);
  errorMessage.set('');
  streamedContent.set('');
}

export function resetAll() {
  file.set(null);
  fileName.set('');
  jobDescription.set('');
  resetAnalysis();
}
