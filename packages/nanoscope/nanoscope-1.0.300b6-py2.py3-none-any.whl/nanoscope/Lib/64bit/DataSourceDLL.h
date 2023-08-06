// Bruker Confidential  
// Copyright 2012. All rights reserved.
//

#if !defined(DataSourceDll_h)
#define DataSourceDll_h

#if defined(DataSourceDll_EXPORTS)
#define DataSourceDllDLLDIR    __declspec(dllexport)   // export DLL information
#else
#define DataSourceDllDLLDIR    __declspec(dllimport)   // import DLL information
#endif 

//note: MAX_STRING_SIZE is the max string size which will be filled and returned (via char* argument) by any function in DataSourceDLL.
//      So anyone calling this should allocate all strings pointers passed in via char* argument, to be this size or larger!!

#define MAX_STRING_SIZE 100


#if defined(__cplusplus)
class DataSourceDllDLLDIR DataSourceDll
{
public:
	DataSourceDll();
	~DataSourceDll(void);
	// For all functions with int return value: return 1 for success, -1 (< 0) upon failure
	static int GetVersionInfo(char* versionInfo);

	static int Open(char * pFileName);
	static int Close();

	enum ScanUnits { VOLTS_UNITS, METRIC_UNITS, FORCE_UNITS, LSB_UNITS };

	//Force data
	static int GetForceCurveData( int ChannelNumber, double * pTrace, double * pRetrace, enum ScanUnits unit );
	//Force Volume image data
	static int GetForceVolumeImageData( double * pImage, int MaxDataSize, int * ActualDataSize, enum ScanUnits unit );
	//Force Volume force curve data
	static int GetForceVolumeForceCurveData( int ChannelNumber, int BufferNumber, double * pTrace, double * pRetrace,
											 int *tracePts, int *retracePts, int MaxDataSize, enum ScanUnits unit );

	//This functions is used to get Hold data from either Force or ForceVolume files. For Force (single curve) files, 
	//parameter BufferNumber is a dummy; and not made not an optional parameter for consistency with other DataSource interfaces
	static int GetForceHoldData(int ChannelNumber, int BufferNumber, double * pHold, enum ScanUnits unit);

	static bool SaveAs16BitData(char* path, bool bSilent = false);

	//These functions are used to get ScriptFile Info and data (after removing padding for incomplete segments)
	static int GetScriptSegmentCount(int* numSegs);
	static int GetScriptSegmentInfo(const int nSegsAlloc, char ** segDescrip, int* segType,  int * segSamps, double * segDuration, double * segSampPeriod,
		int * segTtlOutput);
	static int GetScriptSegmentTimeUnits(const int nSeg, char** segPeriodUnits, char** segDurationUnits);
	static int GetScriptModulationSegmentInfo(const int nSegsAlloc, double * segAmp, double * segFreq, double * segPhaseOffset);
	//static int GetScriptRampSegmentInfo(const int nSegsAlloc, char ** segRampType, double * segRampSize, double * segRampStart);
	static int GetScriptModulationSegmentUnits(const int nSegsAlloc, char ** segAmpUnits, char ** segFreqUnits, char ** segPhaseOFfsetUnits);
	static int GetScriptBiasSegmentInfo(const int nSegsAlloc, double * segTipBias);
	static int GetScriptBiasSegmentUnits(const int nSegsAlloc, char ** segTipBiasUnits);
	static int GetScriptRampSegmentInfo(const int nSegsAlloc, char ** rampType, double * rampSize, double * rampStart);
	static int GetScriptRampSegmentUnits(const int nSegsAlloc, char ** rampSizeUnits, char ** rampStartUnits);

	//This function retreives segment data for all segments (segNumber <=0) or for a specified segment (segNumber > 0) 
	static int GetScriptSegmentData(int ChannelNumber, int segNumber, int nptsAlloc, double * pXvals, double * pYvals, enum ScanUnits unit);

	//Peak force capture z data
	static int GetPeakForceCaptureZData(double * pTrace, double * pRetrace, int tracePts, int retracePts);
	//HSDC data
	static int GetHSDCForceCurveData( int ChannelNumber, double * pBuffer, int MaxDataSize, int * ActualDataSize, enum ScanUnits unit );
	//Image data
	static int GetImageData(int ChannelNumber, double * pBuffer, int MaxDataSize, int * ActualDataSize, enum ScanUnits unit);
	//Parameters
	static int GetSamplesPerLine( int ChannelNumber, int * SamplesPerLine );
	static int GetNumberOfLines( int ChannelNumber, int * NumberOfLines );
	static int GetForceSamplesPerLine( int ChannelNumber, int * SamplesPerLine );
	static int GetNumberOfTracePoints( int ChannelNumber, int * SamplesPerLine);
	static int GetNumberOfHoldPoints( int ChannelNumber, int * NumHoldSamples);
	static int GetForceHoldTime( int ChannelNumber, double * HoldTimeSeconds);
	static int GetNumberOfForceCurves( int * NumberOfCurves );
	static int GetRampModulationInfo(char* rampModType, double* rampModAmp, double* rampModFreq);
	static int GetRampModulationUnits(char* rampModAmpUnits, char* rampModFreqUnits);
	static int GetZSensitivitySoftScale(int ChannelNumber, double* ZSensitivitySoftScale );
	static int GetZSensitivityUnits( int ChannelNumber, char* ZSensitivityUnits);
	static int GetDeflSens(double* deflSens);
	static int GetDeflSensUnits(char* deflSensUnits);
	static int GetDeflLimits(double* deflLimit, double* deflLimitLockin3LSADC1);
	static int GetDeflLimitsUnits(char* deflSensUnits, char* deflLimitLockin3LSADC1Units);
	static int GetNumberOfPointsPerCurve( int ChannelNumber, int * NumberOfPoints );
	static int GetDataBufferSize( int ChannelNumber, int * BufferSize );
	static int GetHsdcScalingFactor( int channel, double * ScalingFactor, bool isMetric = true );
	static int GetScalingFactor( int channel, double * ScalingFactor, bool isMetric = true );
	static int GetExportScalingFactor( int channel, double * ScalingFactor, bool isMetric = true );
	static int GetRampSize( int channel, double * RampSize, bool isMetric = true );
	static int GetZScaleInSwUnits( int channel, double * ZScale );
	static int GetZScaleInHwUnits( int channel, double * ZScale );
	static int GetPoissonRatio( double * PRatio );
	static int GetTipRadius( double * TipRadius );
	static int GetReverseRampVelocity( int Channel, double * Velocity, bool isMetric = true);
	static int GetForwardRampVelocity( int Channel, double * Velocity, bool isMetric = true);
	static int GetForceSpringConstant( int Channel, double * SpringConst );
	static int GetNumberOfChannels( int * NumberOfChannels );
	static int GetRampUnits( int channel, char* rampUnits, bool isMetric = true );
	static int GetDataScaleUnits( int ChannelNumber, char* dataScaleUnits, bool isMetric );
	static int GetDataTypeDesc( int ChannelNumber, char* dataTypeDesc);
	static int GetHalfAngle( double * HalfAngle );
	static int GetHsdcRate(int channel, double * HsdcRate);
	static int GetImageAspectRatio(int channel, double * AspectRatio);
	static int GetPlanefitSettings( int Channel , double * a, double * b, double * c, int * FitType);
	static int GetPeakForceTappingFreq(double *freq);
	static int GetScanSize(int channel, double *scanSize);
	static int GetScanSizeUnit(int channel, char* scanSizeUnit);
	static int GetForcesPerLine(int *forcesPerLine);
	static int GetXYOffsets(double *xOffset, double *yOffset);
	static int GetXYOffsetsUnits(char *xOffsetUnits, char *yOffsetUnits);
	static int GetForceSweepChannel(int ChannelNumber, char*sweepChannel);
	static int GetForceSweepFreqRange(int ChannelNumber, double * fStartHz, double * fStopHz);
	static int GetLineDirection(int channel, char* lineDir);
	static int GetScanLine(int channel, char* scanLine);
	static int GetSegmentDescription(int segType, char* segDescrip);

private:
	//These functions is used internally to retreive the actual file (possibly padded) segment info
	static int GetScriptSegmentFileInfo (const int nSegsAlloc, int * segSamps, int * segSize, int * segType,
												  double * segDuration, double* segSampPeriod, char** durationUnits, char** periodUnits,
												  int * setTtlOutput);
	static int GetScriptSegmentBasicInfo(const int nSegsAlloc, int*  segType, int * segSamps, int* segSize,
												  double * segDuration, double* segSampPeriod,char** durationUnits, char** periodUnits,
												  int * segTtlOutput);
};

#endif

// C wrappers for HarmoniXDll
#if defined(__cplusplus)
extern "C" {
#endif
DataSourceDllDLLDIR int DataSourceDllGetVersionInfo(char* versionInfo);

DataSourceDllDLLDIR int DataSourceDllOpen( char * pFileName );
DataSourceDllDLLDIR int DataSourceDllClose();

//force 
DataSourceDllDLLDIR int DataSourceDllGetForceCurveData( int ChannelNumber, double * pTrace, double * pRetrace );
DataSourceDllDLLDIR int DataSourceDllGetForceCurveMetricData( int ChannelNumber, double * pTrace, double * pRetrace );
DataSourceDllDLLDIR int DataSourceDllGetForceCurveForceData( int ChannelNumber, double * pTrace, double * pRetrace );
DataSourceDllDLLDIR int DataSourceDllGetForceCurveVoltsData( int ChannelNumber, double * pTrace, double * pRetrace );

//force volume
DataSourceDllDLLDIR int DataSourceDllGetForceVolumeImageData( double * pImage, int MaxDataSize, int * ActualDataSize);
DataSourceDllDLLDIR int DataSourceDllGetForceVolumeMetricImageData( double * pImage, int MaxDataSize, int * ActualDataSize);
DataSourceDllDLLDIR int DataSourceDllGetForceVolumeVoltsImageData( double * pImage, int MaxDataSize, int * ActualDataSize);
DataSourceDllDLLDIR int DataSourceDllGetForceVolumeForceCurveData(int ChannelNumber,  int CurveNumber, double * pTrace, double * pRetrace, int * tracePts, int * retracePts, int MaxDataSize);
DataSourceDllDLLDIR int DataSourceDllGetForceVolumeMetricForceCurveData(int ChannelNumber,  int CurveNumber, double * pTrace, double * pRetrace, int * tracePts, int * retracePts, int MaxDataSize);
DataSourceDllDLLDIR int DataSourceDllGetForceVolumeVoltsForceCurveData(int ChannelNumber,  int CurveNumber, double * pTrace, double * pRetrace, int * tracePts, int * retracePts, int MaxDataSize);
DataSourceDllDLLDIR int DataSourceDllGetForceVolumeForceForceCurveData(int ChannelNumber,  int CurveNumber, double * pTrace, double * pRetrace, int * tracePts, int * retracePts, int MaxDataSize);
DataSourceDllDLLDIR int DataSourceDllGetPeakForceCaptureZData(double * pTrace, double * pRetrace, int tracePts, int retracePts);

//force volume data
DataSourceDllDLLDIR int DataSourceDllGetForceHoldData(int ChannelNumber, double * pHold);
DataSourceDllDLLDIR int DataSourceDllGetForceMetricHoldData(int ChannelNumber, double * pHold);
DataSourceDllDLLDIR int DataSourceDllGetForceVoltsHoldData(int ChannelNumber, double * pHold);

//force volume hold data
DataSourceDllDLLDIR int DataSourceDllGetForceVolumeHoldData(int ChannelNumber, int CurveNumber, double * pHold);
DataSourceDllDLLDIR int DataSourceDllGetForceVolumeMetricHoldData(int ChannelNumber, int CurveNumber, double * pHold);
DataSourceDllDLLDIR int DataSourceDllGetForceVolumeVoltsHoldData(int ChannelNumber, int CurveNumber,double * pHold);

//Script segment data
DataSourceDllDLLDIR int DataSourceDllGetScriptSegmentCount(int * nSegs);
DataSourceDllDLLDIR int DataSourceDllGetScriptSegmentInfo(const int nSegs, char ** segDescrip, int* segType,  int * segSamps, double * segDuration, 
	double * segSampPeriod, int * setTtlOutput);
DataSourceDllDLLDIR int DataSourceDllGetScriptSegmentTimeUnits(const int nSeg, char** segDurationUnits, char** segPeriodUnits);
DataSourceDllDLLDIR int DataSourceDllGetScriptModulationSegmentInfo(const int nSegs, double * segAmp, double * segFreq, double * segPhaseOFfset);
DataSourceDllDLLDIR int DataSourceDllGetScriptModulationSegmentUnits(const int nSegs, char ** segAmpUnits, char ** segFreqUnits, char ** segPhaseOFfsetUnits);
DataSourceDllDLLDIR int DataSourceDllGetScriptBiasSegmentInfo(const int nSegs, double * segTipBias);
DataSourceDllDLLDIR int DataSourceDllGetScriptBiasSegmentUnits(const int nSegs, char ** segTipBiasUnits);
DataSourceDllDLLDIR int DataSourceDllGetScriptRampSegmentInfo(const int nSegs, char ** rampType, double * rampSize, double * rampStart);
DataSourceDllDLLDIR int DataSourceDllGetScriptRampSegmentUnits(const int nSegs, char ** rampSizeUnits, char ** rampStartUnits);


DataSourceDllDLLDIR int DataSourceDllGetScriptSegmentData(int ChannelNumber, int segmentNumber, int npts, double * pXData, double * pYData);
DataSourceDllDLLDIR int DataSourceDllGetScriptMetricSegmentData(int ChannelNumber, int segmentNumber, int npts, double * pXData, double * pYData);
DataSourceDllDLLDIR int DataSourceDllGetScriptVoltsSegmentData(int ChannelNumber, int segmentNumber,int npts, double * pXData, double * pYData);

//HSDC
DataSourceDllDLLDIR int DataSourceDllGetHSDCForceCurveData( int ChannelNumber, double * pBuffer, int MaxDataSize, int * ActualDataSize );
DataSourceDllDLLDIR int DataSourceDllGetHSDCMetricForceCurveData( int ChannelNumber, double * pBuffer, int MaxDataSize, int * ActualDataSize );
DataSourceDllDLLDIR int DataSourceDllGetHSDCVoltsForceCurveData( int ChannelNumber, double * pBuffer, int MaxDataSize, int * ActualDataSize );

//Image
DataSourceDllDLLDIR int DataSourceDllGetImageData( int ChannelNumber, double * pBuffer, int MaxDataSize, int * ActualDataSize );
DataSourceDllDLLDIR int DataSourceDllGetImageMetricData( int ChannelNumber, double * pBuffer, int MaxDataSize, int * ActualDataSize );
DataSourceDllDLLDIR int DataSourceDllGetImageVoltsData( int ChannelNumber, double * pBuffer, int MaxDataSize, int * ActualDataSize );

//Parameters
DataSourceDllDLLDIR int DataSourceDllGetForceSamplesPerLine( int ChannelNumber, int * SamplesPerLine );
DataSourceDllDLLDIR int DataSourceDllGetNumberOfTracePoints( int ChannelNumber, int * SamplesPerLine );
DataSourceDllDLLDIR int DataSourceDllGetNumberOfHoldPoints(int ChannelNumber, int * NumHoldSamples);
DataSourceDllDLLDIR int DataSourceDllGetForceHoldTime(int ChannelNumber, double * HoldTimeSeconds);
DataSourceDllDLLDIR int DataSourceDllGetNumberOfPointsPerCurve( int ChannelNumber, int * NumberOfPoints );
DataSourceDllDLLDIR int DataSourceDllGetNumberOfForceCurves(int * NumberOfChannels );
DataSourceDllDLLDIR int DataSourceDllGetRampModulationInfo(char* rampModType, double* rampModAmp, double* rampModFreq);
DataSourceDllDLLDIR int DataSourceDllGetRampModulationUnits(char* rampModAmpUnits, char* rampModFreqUnits);

DataSourceDllDLLDIR int DataSourceDllGetDeflSens(double* deflSens);
DataSourceDllDLLDIR int DataSourceDllGetDeflSensUnits(char* deflSensUnits);
DataSourceDllDLLDIR int DataSourceDllGetDeflLimits(double* deflLimit, double* deflLimitLockin3LSADC1);
DataSourceDllDLLDIR int DataSourceDllGetDeflLimitsUnits(char* deflSensUnits, char* deflLimitLockin3LSADC1Units);
DataSourceDllDLLDIR int DataSourceDllGetZSensitivitySoftScale(int ChannelNumber, double* ZSensitivitySoftScale );
DataSourceDllDLLDIR int DataSourceDllGetZSensitivityUnits( int ChannelNumber, char* ZSensitivityUnits );
DataSourceDllDLLDIR int DataSourceDllGetNumberOfLines( int ChannelNumber, int * NumberOfLines );
DataSourceDllDLLDIR int DataSourceDllGetSamplesPerLine( int ChannelNumber, int * SamplesPerLine );
DataSourceDllDLLDIR int DataSourceDllGetDataBufferSize( int ChannelNumber, int * BufferSize );
DataSourceDllDLLDIR int DataSourceDllGetScalingFactor( int channel, double * ScalingFactor, bool isMetric );
DataSourceDllDLLDIR int DataSourceDllGetExportScalingFactor( int channel, double * ScalingFactor, bool isMetric );
DataSourceDllDLLDIR int DataSourceDllGetMetricDataScaleUnits( int ChannelNumber, char* dataScaleUnits);
DataSourceDllDLLDIR int DataSourceDllGetVoltsDataScaleUnits( int ChannelNumber, char* dataScaleUnits);
DataSourceDllDLLDIR int DataSourceDllGetForceDataScaleUnits( int ChannelNumber, char* dataScaleUnits);
DataSourceDllDLLDIR int DataSourceDllGetDataTypeDesc( int ChannelNumber, char* dataTypeDesc);
DataSourceDllDLLDIR int DataSourceDllGetRampUnits( int ChannelNumber, char* rampUnits, bool isMetric );
DataSourceDllDLLDIR int DataSourceDllGetRampSize( int channel, double * RampSize, bool isMetric);
DataSourceDllDLLDIR int DataSourceDllGetZScaleInSwUnits( int channel, double * ZScale );
DataSourceDllDLLDIR int DataSourceDllGetZScaleInHwUnits( int channel, double * ZScale );
DataSourceDllDLLDIR int DataSourceDllGetTipRadius( double * TipRadius );
DataSourceDllDLLDIR int DataSourceDllGetPoissonRatio( double * PoissonRatio );
DataSourceDllDLLDIR int DataSourceDllGetForwardRampVelocity( int Channel, double * Velocity, bool isMetric );
DataSourceDllDLLDIR int DataSourceDllGetReverseRampVelocity( int Channel, double * Velocity, bool isMetric );
DataSourceDllDLLDIR int DataSourceDllGetForceSpringConstant( int Channel, double * SpringConst);
DataSourceDllDLLDIR int DataSourceDllGetHalfAngle( double * HalfAngle );
DataSourceDllDLLDIR int DataSourceDllGetNumberOfChannels( int * NumberOfChannels );
DataSourceDllDLLDIR int DataSourceDllGetHsdcRate( int Channel, double * HsdcRate);
DataSourceDllDLLDIR int DataSourceDllGetImageAspectRatio( int Channel, double * AspectRatio);
DataSourceDllDLLDIR int DataSourceDllGetPlanefitSettings( int Channel , double * a, double * b, double * c, int * FitType);
DataSourceDllDLLDIR int DataSourceDllGetPeakForceTappingFreq(double * freq); //return peak force tapping frequency in Hz
DataSourceDllDLLDIR int DataSourceDllGetScanSize(int channel, double *scanSize);
DataSourceDllDLLDIR int DataSourceDllGetScanSizeUnit(int channel, char* scanSizeUnit);
DataSourceDllDLLDIR int DataSourceDllGetForcesPerLine(int *forcesPerLine);
DataSourceDllDLLDIR int DataSourceDllGetXYOffsets(double *xOffset, double *yOffset);
DataSourceDllDLLDIR int DataSourceDllGetXYOffsetsUnits(char *xOffsetUnits, char *yOffsetUnits);
DataSourceDllDLLDIR int DataSourceDllGetForceSweepChannel(int ChannelNumber, char* sweepChannel);
DataSourceDllDLLDIR int DataSourceDllGetForceSweepFreqRange(int ChannelNumber, double * fStart, double * fStop);
DataSourceDllDLLDIR int DataSourceDllGetLineDirection(int ChannelNumber, char* lineDirection);
DataSourceDllDLLDIR int DataSourceDllGetScanLine(int ChannelNumber, char* scanLine);
DataSourceDllDLLDIR int DataSourceDllGetSegmentDescription(int SegmentType, char* segDescrip);

#if defined(__cplusplus)
}
#endif

#endif
