//
//  PredictAudioEmotion.swift
//  AudioEmotion
//
//  Created by 杨萧玉 on 2019/3/24.
//  Copyright © 2019 杨萧玉. All rights reserved.
//

import UIKit
import AVFoundation
import CoreML

class PredictAudioEmotion: NSObject {
    let model = AudioEmotion()
    
    func predictAudio(audio fileURL: URL) -> [Dictionary<String, Double>] {
        // Read wav file
        var wavFile:AVAudioFile!
        do {
            wavFile = try AVAudioFile(forReading:fileURL)
        } catch {
            fatalError("Could not open wav file.")
        }
        
        print("wav file length: \(wavFile.length)")
        assert(wavFile.fileFormat.sampleRate==16000.0, "Sample rate is not right!")
        
        let buffer = AVAudioPCMBuffer(pcmFormat: wavFile.processingFormat, frameCapacity: UInt32(wavFile.length))
        do {
            try wavFile.read(into:buffer!)
        } catch{
            fatalError("Error reading buffer.")
        }
        guard let bufferData = buffer?.floatChannelData else {
            fatalError("Can not get a float handle to buffer")
        }
        
        // Chunk data and set to CoreML model
        let windowSize = 15600
        guard let audioData = try? MLMultiArray(shape:[windowSize as NSNumber], dataType:MLMultiArrayDataType.float32) else {
            fatalError("Can not create MLMultiArray")
        }
        
        // Ignore any partial window at the end.
        var windowNumber = 0
        var results = [Dictionary<String, Double>]()
        while ((windowNumber+1) * windowSize) <= (wavFile.length - Int64(windowSize)) {
            let offset = windowNumber * windowSize
            for i in 0...windowSize {
                audioData[i] = NSNumber.init(value: bufferData[0][offset + i])
            }
            let modelInput = AudioEmotionInput(audio: audioData)
            
            guard let modelOutput = try? model.prediction(input: modelInput) else {
                fatalError("Error calling predict")
            }
            results.append(modelOutput.labelProbability)
            windowNumber += 1
        }
        return results
    }
    
    func handlePredictionResults(results: [Dictionary<String, Double>]) -> (label: String, probability: Double) {
        // Average model results from each chunk
        var prob_sums = Dictionary<String, Double>()
        for r in results {
            for (label, prob) in r {
                prob_sums[label] = (prob_sums[label] ?? 0) + prob
            }
        }
        
        var max_sum = 0.0
        var max_sum_label = ""
        for (label, sum) in prob_sums {
            if sum > max_sum {
                max_sum = sum
                max_sum_label = label
            }
        }
        
        let most_probable_label = max_sum_label
        let probability = max_sum / Double(prob_sums.count)
        print("\(most_probable_label) predicted, with probability: \(probability)")
        return (most_probable_label, probability)
    }
}
