<script lang="ts">
  import type { AnalysisResult } from '$lib/types';
  import ScoreRing from './ScoreRing.svelte';
  import KeywordMatches from './KeywordMatches.svelte';
  import WeakPhrases from './WeakPhrases.svelte';
  import Suggestions from './Suggestions.svelte';
  import Strengths from './Strengths.svelte';

  interface Props {
    result: AnalysisResult;
  }

  let { result }: Props = $props();
</script>

<div class="space-y-6 animate-in">
  <!-- Header: Score + Summary -->
  <div class="flex flex-col items-center gap-6 rounded-xl border border-zinc-700/50 bg-zinc-800/30 p-6 sm:flex-row sm:items-start">
    <ScoreRing score={result.overall_score} />
    <div class="flex-1 text-center sm:text-left">
      <h2 class="mb-2 text-xl font-bold text-zinc-100">Analysis Complete</h2>
      <p class="text-sm leading-relaxed text-zinc-400">{result.summary}</p>
    </div>
  </div>

  <!-- Strengths -->
  {#if result.strengths.length > 0}
    <Strengths strengths={result.strengths} />
  {/if}

  <!-- Keywords -->
  <KeywordMatches keywords={result.keyword_matches} />

  <!-- Weak Phrases -->
  <WeakPhrases phrases={result.weak_phrases} />

  <!-- Suggestions -->
  <Suggestions suggestions={result.suggestions} />
</div>

<style>
  .animate-in {
    animation: fadeSlideIn 0.4s ease-out;
  }

  @keyframes fadeSlideIn {
    from {
      opacity: 0;
      transform: translateY(12px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>
