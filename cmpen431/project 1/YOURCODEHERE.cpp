#include <iostream>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <sys/stat.h>
#include <unistd.h>
#include <algorithm>
#include <fstream>
#include <map>
#include <math.h>
#include <fcntl.h>
#include <vector>
#include <iterator>

#include "431project.h"

using namespace std;

/*
 * Enter your PSU IDs here to select the appropriate scanning order.
 */
#define PSU_ID_SUM (908727073)
// 908727073 % 24 = 1 --> BP Cache FPU Core

/*
 * Some global variables to track heuristic progress.
 * 
 * Feel free to create more global variables to track progress of your
 * heuristic.
 */
unsigned int getil1size(std::string configuration);
unsigned int getdl1size(std::string configuration);
unsigned int getl2size(std::string configuration);

bool currentDimDone = false;
bool isDSEComplete = false;
int exploreOrder[] = {12, 13, 14, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1};
int index = 0;
unsigned int currentlyExploringDim = exploreOrder[0];
int explored[] = {-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1};
bool best = false;


/*
 * Given a half-baked configuration containing cache properties, generate
 * latency parameters in configuration string. You will need information about
 * how different cache paramters affect access latency.
 * 
 * Returns a string similar to "1 1 1"
 */
std::string generateCacheLatencyParams(string halfBackedConfig) {

	unsigned int il1 = getil1size(halfBackedConfig);
	unsigned int dl1 = getdl1size(halfBackedConfig);
	unsigned int ul2 = getl2size(halfBackedConfig);

	int il1lat;
	int dl1lat;
	int ul2lat;

	if(il1 <= 2048)
		il1lat = 1;
	else if(il1 <= 4096)
		il1lat = 2;
	else if(il1 <= 8192)
		il1lat = 3;
	else if(il1 <= 16384)
		il1lat = 4;
	else if(il1 <= 32768)
		il1lat = 5;
	else if(il1 <= 65536)
		il1lat = 6;

	if(dl1 <= 2048)
		dl1lat = 1;
	else if(dl1 <= 4096)
		dl1lat = 2;
	else if(dl1 <= 8192)
		dl1lat = 3;
	else if(dl1 <= 16384)
		dl1lat = 4;
	else if(dl1 <= 32768)
		dl1lat = 5;
	else if(dl1 <= 65536)
		dl1lat = 6;

	if(ul2 <= 32768)
		ul2lat = 5;
	else if(ul2 <= 65536)
		ul2lat = 6;
	else if(ul2 <= 131072)
		ul2lat = 7;
	else if(ul2 <= 262144)
		ul2lat = 8;
	else if(ul2 <= 524288)
		ul2lat = 9;
	else if(ul2 <= 1048576)
		ul2lat = 10;

	unsigned int il1assoc = 1 << extractConfigPararm(halfBackedConfig, 6);
	unsigned int dl1assoc = 1 << extractConfigPararm(halfBackedConfig, 4);
	unsigned int ul2assoc = 1 << extractConfigPararm(halfBackedConfig, 9);

	if(il1assoc == 2)
		il1lat++;
	else if(il1assoc == 4)
		il1lat += 2;

	if(dl1assoc == 2)
		dl1lat++;
	else if(dl1assoc == 4)
		dl1lat += 2;

	if(ul2assoc == 2)
		ul2lat++;
	else if(ul2assoc == 4)
		ul2lat += 2;
	else if(ul2assoc == 8)
		ul2lat += 3;
	else if(ul2assoc == 16)
		ul2lat += 4;

	std::stringstream ss;

	ss << il1lat << " " << dl1lat << " " << (ul2lat - 5);

	return ss.str();
}

/*
 * Returns 1 if configuration is valid, else 0
 */
int validateConfiguration(std::string configuration) {

	int width = 1 << extractConfigPararm(configuration, 0);
	unsigned int il1blocksize = 8 * (1 << extractConfigPararm(configuration, 2));

	if(il1blocksize < width * 8)
		return 0;

	unsigned int l2blocksize = 16 << extractConfigPararm(configuration, 8);

	if(l2blocksize < il1blocksize * 2)
		return 0;

	unsigned int il1 = getil1size(configuration);

	if(il1 < 2048 || il1 > 65536)
		return 0;

	unsigned int dl1 = getdl1size(configuration);

	if(dl1 < 2048 || dl1 > 65536)
		return 0;

	unsigned int ul2 = getl2size(configuration);

	if(ul2 < 32768 || ul2 > 1048576)
		return 0;

	// The below is a necessary, but insufficient condition for validating a
	// configuration.

	return isNumDimConfiguration(configuration);
}

/*
 * Given the current best known configuration, the current configuration,
 * and the globally visible map of all previously investigated configurations,
 * suggest a previously unexplored design point. You will only be allowed to
 * investigate 1000 design points in a particular run, so choose wisely.
 *
 * In the current implementation, we start from the leftmost dimension and
 * explore all possible options for this dimension and then go to the next
 * dimension until the rightmost dimension.
 */
std::string generateNextConfigurationProposal(std::string currentconfiguration,
		std::string bestEXECconfiguration, std::string bestEDPconfiguration,
		int optimizeforEXEC, int optimizeforEDP) {

	//
	// Some interesting variables in 431project.h include:
	//
	// 1. GLOB_dimensioncardinality
	// 2. GLOB_baseline
	// 3. NUM_DIMS
	// 4. NUM_DIMS_DEPENDENT
	// 5. GLOB_seen_configurations

	//12-14
	//2-10
	//11-11
	//0-1

	std::string nextconfiguration = currentconfiguration;
	// Continue if proposed configuration is invalid or has been seen/checked before.
	while (!validateConfiguration(nextconfiguration) ||
		GLOB_seen_configurations[nextconfiguration]) {

		// Check if DSE has been completed before and return current
		// configuration.
		if(isDSEComplete) {
			return currentconfiguration;
		}

		std::stringstream ss;

		string bestConfig;
		if (optimizeforEXEC == 1)
			bestConfig = bestEXECconfiguration;

		if (optimizeforEDP == 1)
			bestConfig = bestEDPconfiguration;

		for(int i = 0; i < 15; i++) {
			if(explored[i] == 1) {
				ss << extractConfigPararm(bestConfig, i) << " ";
			} else {
				if(i == currentlyExploringDim) {
					if(explored[i] == -1) {
						ss << "0 ";
						explored[i] = 0;
					} else {
						int nextValue = extractConfigPararm(nextconfiguration, currentlyExploringDim) + 1;

						if (nextValue >= GLOB_dimensioncardinality[currentlyExploringDim]) {
							nextValue = GLOB_dimensioncardinality[currentlyExploringDim] - 1;
							currentDimDone = true;
						}

						ss << nextValue << " ";
					}
				} else {
					ss << extractConfigPararm(currentconfiguration, i) << " ";
				}
			}
		}		

		string configSoFar = ss.str();

		ss << generateCacheLatencyParams(configSoFar);

		nextconfiguration = ss.str();

		if (currentDimDone) {
			explored[currentlyExploringDim] = 1;
			index++;
			currentlyExploringDim = exploreOrder[index];
			currentDimDone = false;
		}

		// Signal that DSE is complete after this configuration.
		if (index == (NUM_DIMS - NUM_DIMS_DEPENDENT)) {
			if(best) {
				isDSEComplete = true;
			} else {
				for(int i = 0; i < 15; i++) {
					explored[i] = -1;
				}
				index = 0;
				currentlyExploringDim = exploreOrder[index];
				best = true;
			}
		}
	}
	return nextconfiguration;
}