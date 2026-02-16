<script lang="ts">
  interface Props {
    strengths: string[];
  }

  let { strengths }: Props = $props();
</script>

<section class="rounded-xl border border-zinc-700/50 bg-zinc-800/30 p-6">
  <h3 class="mb-4 text-lg font-semibold text-zinc-100">Strengths</h3>

  <div class="space-y-2">
    {#each strengths as strength}
      <div class="flex items-start gap-3 rounded-lg bg-emerald-500/5 px-4 py-3">
        <svg class="mt-0.5 h-4 w-4 shrink-0 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
        </svg>
        <p class="text-sm text-zinc-300">{strength}</p>
      </div>
    {/each}
  </div>
</section>
