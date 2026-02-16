<script lang="ts">
  import { jobDescription, resetAnalysis } from '$lib/stores';

  function handleInput(e: Event) {
    const target = e.target as HTMLTextAreaElement;
    jobDescription.set(target.value);
    resetAnalysis();
  }

  let charCount = $derived($jobDescription.length);
</script>

<div class="space-y-2">
  <label class="block text-sm font-medium text-zinc-300" for="job-description">
    Job Description
  </label>
  <textarea
    id="job-description"
    value={$jobDescription}
    oninput={handleInput}
    placeholder="Paste the full job description here..."
    rows="8"
    class="w-full resize-y rounded-lg border border-zinc-600 bg-zinc-800/50 px-4 py-3 text-sm text-zinc-200 placeholder-zinc-500 transition-colors focus:border-amber-400/50 focus:outline-none focus:ring-1 focus:ring-amber-400/20"
  ></textarea>
  <div class="flex justify-between text-xs text-zinc-500">
    <span>{charCount > 20 ? 'Ready to analyse' : 'Minimum 20 characters'}</span>
    <span>{charCount} chars</span>
  </div>
</div>
