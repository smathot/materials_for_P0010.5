---
title:
 "Large Pupils Predict Goal-driven Eye Movements (supplementary material)"
author:
  Sebastiaan Mathôt^1^, Alisha Siebold^2^, Mieke Donk^2^, and Françoise Vitu^1^
affiliation:
 - ^1^ Aix-Marseille University, CNRS, LPC UMR 7290, Marseille, France
 - ^2^ Dept. of Cognitive Psychology, VU University Amsterdam
correspondence:
 - Aix-Marseille University, CNRS
 - Laboratoire de Psychologie Cognitive, UMR 7290
 - 3 Place Victor Hugo
 - Centre St. Charles, Bâtiment 9, Case D
 - 13331 Marseille
 - France
---

# Materials

Analysis scripts, data, stimuli (where possible given license restrictions), saliency maps, and luminance maps are available from <http://to.do/>.

# Linear mixed-effects models

The procedure used to construct the linear mixed-effects models (LME) is described in the main text. Models were estimated using the `lmer()` function from the `lme4` [v1.0, @Bates2014] package for R (v3.0.2).

%--
table:
 id: TblExp1
 source: exp1.csv
 caption:
  The LME for Exp. 1 used to estimate the partial slope of the relationship between pupil size and fixation saliency.
--%

%--
table:
 id: TblExp2
 source: exp2.csv
 caption:
  The LME for Exp. 2 used to estimate the partial slope of the relationship between pupil size and fixation saliency.
--%

%--
table:
 id: TblExp2Int
 source: exp2.int.csv
 caption:
  The LME for Exp. 2, including effects of stimulus type, pupil size, and relevant interaction terms. Fractals are used as reference stimulus type. Free-viewing is used as reference task instruction.
--%

%--
table:
 id: TblExp3
 source: exp3.csv
 caption:
  The LME for Exp. 3 used to estimate the partial slope of the relationship between pupil size and fixation saliency.
--%

%--
table:
 id: TblExp3Int
 source: exp3.int.csv
 caption:
  The LME for Exp. 3, including the effects of task instruction and task instruction x pupil size interaction. Dual task is used as reference task instruction.
--%

# Relationship between luminance and saliency

It is well known that luminance is the primary determinant of pupil size [e.g., @Ellis1981]: The pupil constricts when looking at, or even attending to [@Binda2013Neurosci;@Mathôt2013Plos], bright surfaces. Therefore, if luminance were consistently and positively correlated with visual saliency, and if this were not controlled for, a pupillary light response might fully explain our results. Our primary way to control for this potential confound is by estimating pupillary luminance maps, and entering values from these maps as fixed effects into the models, as described above and in the main text.

%--
figure:
 id: FigLumSal
 source: FigLumSal.svg
 caption: |
  The correlation between visual saliency and luminance. Dots correspond to individual images. a) The 200 images used for Exp. 1 and 3. b) The 50 natural scenes used for Exp. 2. c) The 50 3D fractals used for Exp. 2.
--%

However, it is also informative to directly consider the relation between luminance and saliency, in order to dispel any lingering suspicion that this may have confounded our results. As can be seen in %FigLumSal (see also the factor 'Fixation luminance' in Tables 1-3), the direction of this correlation varies widely from image to image, and also between the different image sets. (The values on the x-axis indicate the correlation coefficient between saliency and luminance values for the same pixel, separately for each image.) For the photos from the UPenn natural image database [@Tkačik2011], there was a weak negative correlation (a two-sided one-sample t-test against 0 on the correlation coefficients for each image: M = -.059, SE = .023, t(199) = 2.580, p = .011). This may reflect the fact that the primary source of brightness in the savanna is the sky, which is not very salient. For the images from the Campus Scene collection [@BurgeGeisler2011], there was a moderate positive correlation (M = .338, SE = 0.032, t(49) = 10.420, p < .001). This presumably reflects the fact that these images were taken in an urbanized environment, where bright lights are a dominant source of saliency. For the 3D Mandelbulber-generated fractals [@Marczak2012], there was also a moderate positive correlation (M = 0.272, SE = 0.043, t(49) = 6.259, p < 0.001), presumably due to the use of virtual light sources.

For our purpose, the crucial point to note is that the correlation between saliency and brightness is variable, and can be positive or negative depending on the specifics of the stimuli. However, the correlation between pupil size and saliency is invariably negative, and can therefore not be (fully) related to brightness.

# Correlation between pupil size and saliency

For our main analyses, we report the LME slopes of the relationship between transformed pupil size and fixation saliency. This is statistically appropriate, because transforming pupil size increases statistical power, and using partial effects allows us to take into account that the data points (fixations) are not independent. However, it is also informative to simply consider the correlation between pupil size and fixation saliency to see what this relationship 'really' looks like. This is shown in %FigCorrelation. Fixation saliency is not normally distributed, but is dominated by 0 values, which makes the overall pattern difficult to appreciate visually. However, the negative correlation is visible as a slightly asymmetry in the heatmap of the 2D histogram.

%--
figure:
 id: FigCorrelation
 source: FigCorrelation.svg
 caption: |
  The correlation between pupil size and fixation saliency for Exp 1., Exp. 2, and the two conditions from Exp. 3. The heatmap corresponds to a 2D histogram, where white indicates a cell count of 0. The regression line corresponds to a linear regression.
--%

# Acknowledgements

%-- include: md/acknowledgements.md --%
