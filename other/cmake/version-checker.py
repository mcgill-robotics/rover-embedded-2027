# Designed to be called by CMake in version-checker.cmake
# This script must have a non-exit code on failure for CMake to catch the error
# Call with arguments Actual_Version, Expected_Version, Policy
# policy should be EXACT, APPROX or ANY
# APPROX needs a higher actual patch number
# 0 on success
# 1 on version mismatch
# 22 on bad arguments (not enough or bad policy)

import sys
import string
import re

# Regex from https://semver.org/
semver_regex = re.compile(r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$")

def get_semver(version):
	version = version.strip()
	if version.startswith("v"):
		version = version[1:]
	match = semver_regex.match(version)
	if match is None:
		return None
	return {
		"major":match.group("major"), 
		"minor":match.group("minor"), 
		"patch":match.group("patch"), 
		"prerelease":match.group("prerelease"), 
		"build":match.group("buildmetadata")
	}

# # Must provide expected, actual, match mode
if len(sys.argv) != 4:
	print(f"Bad argument count: (Need: 3 Got: {len(sys.argv)-1})", file=sys.stderr)
	exit(22)


# Actual, Expected, Policy
version_1 = sys.argv[1]
version_2 = sys.argv[2]
match_mode = sys.argv[3]

version_1_semver = get_semver(version_1)
version_2_semver = get_semver(version_2)

mismatch_message = f"Version Mismatch: (Found: {version_1}, Expected: {version_2}) with policy {match_mode}"

if version_1_semver is None or version_2_semver is None:
	# if not semver ignore match mode and do exact match
	if version_1 == version_2:
		exit(0)
	print("Non Semantic Versioning detected, falling back to exact match")
	print(mismatch_message, file=sys.stderr)
	exit(1)
if match_mode == "ANY":
	exit(0)
elif match_mode == "EXACT":
	# everything except for build must match
	if (version_1_semver["major"] == version_2_semver["major"] 
		and version_1_semver["minor"] == version_2_semver["minor"] 
		and version_1_semver["patch"] == version_2_semver["patch"] 
		and version_1_semver["prerelease"] == version_2_semver["prerelease"]):
		exit(0)
	print(mismatch_message, file=sys.stderr)
	exit(1)
elif match_mode == "APPROX":
	# Patch must be equal or above
	# Does check the prerelease and should be equal
	# Build is always ignored
	if (version_1_semver["major"] == version_2_semver["major"] 
		and version_1_semver["minor"] == version_2_semver["minor"] 
		and version_1_semver["patch"] >= version_2_semver["patch"] 
		and version_1_semver["prerelease"] == version_2_semver["prerelease"]):
		exit(0)
	print(mismatch_message, file=sys.stderr)
	exit(1)
else:
	print(f"Bad Policy: (Got: {match_mode}, Expected: [EQUAL|APPROX|ANY])", file=sys.stderr)
	exit(22)

# UNUSED PARSER FOR SEMVER
# Not extensively tested
# Kept here just in case but the regex should handle everything fine

# class SemVerParser:
# 	"""
# 	Recursive Descent parser for Semantic Versioning
# 	Based on the Backus-Naur Form grammar found here https://semver.org/
# 	also allows leading 'v' in version names
# 	"""

# 	positive_digits = "1234456789"
# 	non_digit = string.ascii_letters+"-"
# 	alphanum = non_digit+string.digits

# 	def __init__(self, version_string):
# 		self.errors = 0
# 		self.version_string = version_string
# 		self.index = 0

# 	def next_c(self):
# 		if self.index >= len(self.version_string):
# 			return None
# 		c = self.version_string[self.index]
# 		self.index+=1
# 		return c

# 	def lookahead_c(self, n):
# 		if self.index+n >= len(self.version_string):
# 			return None
# 		return self.version_string[self.index+n]

# 	def expect(self, expected):
# 		actual = self.next_c()
# 		if actual is None:
# 			return actual, False
# 		if actual not in expected:
# 			self.errors+=1
# 		return actual, actual in expected

# 	def match_c(self, expected):
# 		actual = self.lookahead_c(0)
# 		if actual is None:
# 			return actual, False
# 		return actual, actual in expected

# 	def parse(self):
# 		# Allow optional leading v
# 		if self.lookahead_c(0) == "v":
# 			self.next_c()

# 		version_core = self.version_core()
# 		pre_release = None
# 		build = None
# 		if version_core is None:
# 			return None
# 		if self.lookahead_c(0) == "-":
# 			self.next_c()
# 			pre_release = self.pre_release()
# 			if pre_release is None:
# 				return None
# 		if self.lookahead_c(0) == "+":
# 			self.next_c()
# 			build = self.build()
# 			if build is None:
# 				return None
# 		if self.lookahead_c(0) is not None or self.errors > 0:
# 			return None
# 		return (version_core[0], version_core[1], version_core[2], pre_release, build)
	
# 	def pre_release(self):
# 		# dot separated pre_release_id
# 		full_id = []
# 		while True:
# 			pr_id = self.pre_release_id()
# 			if pr_id is None:
# 				return None
# 			full_id.append(pr_id)
# 			if self.lookahead_c(0) == ".":
# 				full_id.append(self.next_c())
# 				continue
# 			break
# 		return "".join(full_id)

# 	def build(self):
# 		# dot separated build_id
# 		full_id = []
# 		while True:
# 			b_id = self.build_id()
# 			if b_id is None:
# 				return None
# 			full_id.append(b_id)
# 			if self.lookahead_c(0) == ".":
# 				full_id.append(self.next_c())
# 				continue
# 			break
# 		return "".join(full_id)

# 	def pre_release_id(self):
# 		# not exactly following a recursive descent parser
# 		# cheat by checking for illegal input with leading zeros only
# 		chars = []
# 		isNumeric = True
# 		hasLeadingZero =  self.lookahead_c(0) == "0"
# 		while True:
# 			c, ok = self.match_c(self.alphanum)
# 			if ok:
# 				self.next_c()
# 				if c in self.non_digit:
# 					isNumeric = False
# 				chars.append(c)
# 			else:
# 				break
# 		if isNumeric and hasLeadingZero:
# 			self.errors+=1
# 			return None
# 		if chars:
# 			return "".join(chars)
# 		else:
# 			self.errors+=1
# 			return None


# 	def build_id(self):
# 		# Allow any sequence of  letter, digit or -
# 		chars = []
# 		while True:
# 			c, ok = self.match_c(self.alphanum)
# 			if ok:
# 				self.next_c()
# 				chars.append(c)
# 			else:
# 				break
# 		if chars:
# 			return "".join(chars)
# 		else:
# 			self.errors+=1
# 			return None

# 	def version_core(self):
# 		major = self.numeric_id()
# 		if major is None:
# 			return None
# 		self.expect(".")
# 		minor = self.numeric_id()
# 		if minor is None:
# 			return None
# 		self.expect(".")
# 		patch = self.numeric_id()
# 		if patch is None:
# 			return None
# 		return (major, minor, patch)

# 	def digits(self):
# 		nums = []
# 		while True:
# 			c, ok = self.match_c(string.digits)
# 			if ok:
# 				self.next_c()
# 				nums.append(c)
# 			else:
# 				break
# 		return nums

# 	def numeric_id(self):
# 		# cannot have leading zeros
# 		if self.lookahead_c(0) == "0":
# 			self.next_c()
# 			return 0
# 		else:
# 			c, ok = self.expect(self.positive_digits)
# 			if ok:
# 				version_num = [c]
# 				version_num.extend(self.digits())
# 				return int("".join(version_num))
# 			return None
