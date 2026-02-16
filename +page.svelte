<script lang="ts">
  import FileUpload from '$lib/components/FileUpload.svelte';
  import JobDescriptionInput from '$lib/components/JobDescriptionInput.svelte';
  import AnalysisLoader from '$lib/components/AnalysisLoader.svelte';
  import AnalysisResults from '$lib/components/AnalysisResults.svelte';
  import {
    file,
    jobDescription,
    analysisState,
    analysisResult,
    errorMessage,
    canSubmit,
    resetAll,
  } from '$lib/stores';
  import { analyseResume } from '$lib/utils/api';

  async function handleAnalyse() {
    const currentFile = $file;
    const currentJD = $jobDescription;

    if (!currentFile || !currentJD.trim()) return;

    analysisState.set('uploading');
    errorMessage.set('');
    analysisResult.set(null);

    // Small delay for UX
    await new Promise((r) => setTimeout(r, 300));
    analysisState.set('streaming');

    await analyseResume(
      currentFile,
      currentJD,
      () => {
        // onChunk: could update a progress indicator here
      },
      (result) => {
        analysisResult.set(result);
        analysisState.set('complete');
      },
      (error) => {
        errorMessage.set(error);
        analysisState.set('error');
      }
    );
  }
</script>

<svelte:head>
  <title>ResumeAI - AI-Powered Resume Feedback</title>
  <meta name="description" content="Get instant AI feedback on your resume against any job description" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
</svelte:head>

<main class="mx-auto max-w-3xl px-4 py-12 font-['DM_Sans',sans-serif] sm:px-6 lg:px-8">
  <!-- Header -->
  <header class="mb-10 text-center">
    <div class="mb-3 inline-flex items-center gap-2 rounded-full border border-amber-500/20 bg-amber-500/5 px-4 py-1.5">
      <div class="h-2 w-2 animate-pulse rounded-full bg-amber-400"></div>
      <span class="text-xs font-medium text-amber-300">Powered by Claude AI</span>
    </div>
    <h1 class="mb-3 text-4xl font-bold tracking-tight text-zinc-50 sm:text-5xl">
      Resume<span class="text-amber-400">AI</span>
    </h1>
    <p class="mx-auto max-w-lg text-base text-zinc-400">
      Upload your resume and paste a job description. Get instant, actionable feedback to land the interview.
    </p>
  </header>

  <!-- Input Section -->
  {#if $analysisState !== 'complete'}
    <div class="space-y-6">
      <FileUpload />
      <JobDescriptionInput />

      <!-- Error display -->
      {#if $errorMessage}
        <div class="rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-300">
          {$errorMessage}
        </div>
      {/if}

      <!-- Submit button -->
      <button
        onclick={handleAnalyse}
        disabled={!$canSubmit}
        class="w-full rounded-lg px-6 py-3.5 text-sm font-semibold transition-all duration-200 disabled:cursor-not-allowed disabled:opacity-40 {$canSubmit
          ? 'bg-amber-500 text-zinc-900 hover:bg-amber-400 active:bg-amber-600'
          : 'bg-zinc-700 text-zinc-400'}"
      >
        {#if $analysisState === 'uploading' || $analysisState === 'analysing' || $analysisState === 'streaming'}
          Analysing...
        {:else}
          Analyse My Resume
        {/if}
      </button>
    </div>

    <!-- Loading state -->
    <AnalysisLoader />
  {/if}

  <!-- Results Section -->
  {#if $analysisState === 'complete' && $analysisResult}
    <div class="space-y-6">
      <AnalysisResults result={$analysisResult} />

      <!-- Start over -->
      <div class="flex justify-center pt-4">
        <button
          onclick={resetAll}
          class="rounded-lg border border-zinc-600 px-6 py-2.5 text-sm font-medium text-zinc-300 transition-colors hover:border-zinc-400 hover:text-zinc-100"
        >
          Analyse Another Resume
        </button>
      </div>
    </div>
  {/if}

  <!-- Footer -->
  <footer class="mt-16 border-t border-zinc-800 pt-6 text-center text-xs text-zinc-600">
    <p>Your resume is never stored. All processing happens in-memory and is discarded after analysis.</p>
    <p class="mt-1">Built with SvelteKit, FastAPI & Claude AI</p>
  </footer>
</main>
