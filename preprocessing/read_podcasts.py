import pandas as pd
import glob
import json
import os

from tqdm import tqdm

class PodcastClaims: 

	# transcript claims 
	def __init__(self, show_uri, episode_uri, transcript_claims):
		self.show_uri = show_uri
		self.episode_uri = episode_uri
		self.transcript_claims = transcript_claims

	def divide_claims(self, surrounding_context=2):
		divided_claims = []

		# pad claims, prepend and extend empty strings to array
		temp_claims = self.transcript_claims.copy()
		temp_claims[:0] = ['SEP'] * surrounding_context
		temp_claims[len(temp_claims):] = ['SEP'] * surrounding_context

		for idx in range(len(self.transcript_claims)):

			# print((idx, 2 * surrounding_context + 1))
			# print(temp_claims[idx:2 * surrounding_context + 1])

			divided_claims.append(temp_claims[idx: idx + 2 * surrounding_context + 1])

		return divided_claims


def main(podcast_dir="../podcasts-no-audio-13GB/spotify-podcasts-2020", surrounding_context=2):
	
	# Find all podcasts (.json files) in subdirectory
	podcast_filepaths = glob.glob(podcast_dir + "/**/*.json", recursive=True)

	# Read each podcast, concatenate all the transcript claims, then save claims 
	## NOTE: A transcript claim is a sentence > 5 words within the podcast 

	for podcast_fp in tqdm(podcast_filepaths):
		podcast = read_transcript(podcast_fp)
		save_transcript(podcast, surrounding_context=surrounding_context)
		break

# saves transcript claims in a tsv (tab separated file)
# line format is show_uri, episode_uri, context_claims
def save_transcript(podcast, surrounding_context=2):

	save_dir = f"./outputs"

	if not os.path.isdir(save_dir):
		os.mkdir(save_dir)

	save_fp = f"{save_dir}/podcast_claims_context_{surrounding_context}.tsv"

	divided_claims = podcast.divide_claims(surrounding_context=surrounding_context)

	with open(save_fp, 'a') as f:
		for dc in divided_claims:
			save_str = f"{podcast.show_uri}\t{podcast.episode_uri}\t"
			save_str += "\t".join(dc) + "\n"
			f.write(save_str)

def read_transcript(podcast_fp):
	claims = []
	data = []

	# define episode and show uri
	path, episode_uri = os.path.split(podcast_fp)
	episode_uri = os.path.splitext(episode_uri)[0]
	_, show_uri = os.path.split(path)

	with open(podcast_fp, 'r') as f:
		data = json.load(f)

	for results in data['results']:
		if 'transcript' in results['alternatives'][0]:
			claims.extend(clean_and_filter_claims(results['alternatives'][0]['transcript'].split('.')))

	return PodcastClaims(show_uri=show_uri, episode_uri=episode_uri, transcript_claims=claims)

# claims is an array of strings (each claim is a sentence within the podcast transcript)
def clean_and_filter_claims(claims):
	temp_claims = []

	for claim in claims:

		# replace tabs with spaces
		temp_claim = claim.replace('\t', ' ')

		# filter claims based on amount of words
		if len(temp_claim.split(" ")) < 5:
			continue

		temp_claims.append(temp_claim)

	return temp_claims

if __name__ == "__main__":
	main(podcast_dir="../podcasts-no-audio-13GB/spotify-podcasts-2020", surrounding_context=2)